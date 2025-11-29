import os
import smtplib
import ssl
from typing import List
from datetime import datetime
from email.message import EmailMessage

from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv
from pydantic import BaseModel

from .models import Base, Product, PriceLog
from .scraper import fetch_amazon_price

# --- CONFIG ---
load_dotenv()
SQLALCHEMY_DATABASE_URL = "sqlite:///./data/tracker.db"
from fastapi import FastAPI, Depends

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="🛒 Amazon Price Tracker API",
    description="Monitor multiple Amazon products and get alerts when prices drop.",
    version="2.0"
)
scheduler = BackgroundScheduler()

# --- Pydantic Schemas (Input Validation) ---
class ProductCreate(BaseModel):
    title: str
    url: str
    target_price: float

class ProductResponse(ProductCreate):
    id: int
    last_price: float | None = None
    last_check: datetime | None = None
    
    class Config:
        from_attributes = True

class PriceLogResponse(BaseModel):
    id: int
    product_id: int
    price: float
    timestamp: datetime
    
    class Config:
        from_attributes = True

# --- Dependency ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- NOTIFICATION LOGIC ---
def send_email_alert(product_title: str, current_price: float, link: str):
    """Send email notification when price drops below target."""
    sender = os.getenv('EMAIL_USER')
    password = os.getenv('EMAIL_PASS')
    receiver = os.getenv('EMAIL_RECEIVER')
    
    if not sender or not password:
        print("[!] Skipping email: Credentials missing in .env")
        return

    msg = EmailMessage()
    msg['Subject'] = f"🚨 Price Drop Alert: {product_title} is ₹{current_price}!"
    msg['From'] = sender
    msg['To'] = receiver
    msg.set_content(f"Great news! The price for {product_title} has dropped to ₹{current_price}!\n\nBuy Now: {link}")

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender, password)
            server.sendmail(sender, receiver, msg.as_string())
        print(f"[v] Email sent for {product_title}")
    except Exception as e:
        print(f"[!] Email error: {e}")

# --- SCHEDULER TASKS ---
def check_prices_job():
    """Background job: Checks all products in DB and sends alerts."""
    db = SessionLocal()
    try:
        products = db.query(Product).all()
        print(f"\n[*] --- Starting Price Check Job ({len(products)} products) ---")
        
        for p in products:
            new_price = fetch_amazon_price(p.url)
            if new_price:
                # 1. Update Product Status
                p.last_price = new_price
                p.last_check = datetime.utcnow()
                
                # 2. Log History
                log = PriceLog(product_id=p.id, price=new_price)
                db.add(log)
                
                # 3. Check Condition & Alert
                if new_price <= p.target_price:
                    print(f"[!] 💰 DEAL FOUND: {p.title} at ₹{new_price} (Target: ₹{p.target_price})")
                    send_email_alert(p.title, new_price, p.url)
                else:
                    print(f"[+] {p.title}: ₹{new_price} (Target: ₹{p.target_price})")
        
        db.commit()
        print("[*] --- Price Check Complete ---\n")
    except Exception as e:
        print(f"[!] Job error: {e}")
    finally:
        db.close()

# --- LIFECYCLE EVENTS ---
@app.on_event("startup")
def startup_event():
    """Initialize scheduler on startup."""
    scheduler.add_job(check_prices_job, 'interval', hours=1, id='price_check')
    scheduler.start()
    print("[v] Scheduler started - checks every 1 hour")

@app.on_event("shutdown")
def shutdown_event():
    """Gracefully shutdown scheduler."""
    scheduler.shutdown()
    print("[*] Scheduler shutdown")

# --- ENDPOINTS ---

@app.get("/", tags=["Health"])
def home():
    """API health check."""
    return {
        "status": "✅ Active",
        "message": "Visit /docs for interactive API documentation",
        "endpoints": ["/products", "/products/{id}/history", "/trigger-scan"]
    }

@app.post("/products", response_model=ProductResponse, tags=["Products"])
def add_product(product: ProductCreate, db: Session = Depends(get_db)):
    """Add a new Amazon product to track."""
    # Check if URL already exists
    existing = db.query(Product).filter(Product.url == product.url).first()
    if existing:
        raise HTTPException(status_code=400, detail="Product URL already tracked")
    
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    
    # Trigger immediate price check
    price = fetch_amazon_price(db_product.url)
    if price:
        db_product.last_price = price
        db_product.last_check = datetime.utcnow()
        db.commit()
        print(f"[+] Product added: {db_product.title} at ₹{price}")
    
    return db_product

@app.get("/products", response_model=List[ProductResponse], tags=["Products"])
def get_products(db: Session = Depends(get_db)):
    """List all tracked products."""
    return db.query(Product).all()

@app.get("/products/{product_id}", response_model=ProductResponse, tags=["Products"])
def get_product(product_id: int, db: Session = Depends(get_db)):
    """Get details of a specific product."""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.delete("/products/{product_id}", tags=["Products"])
def delete_product(product_id: int, db: Session = Depends(get_db)):
    """Remove a product from tracking."""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    db.delete(product)
    db.commit()
    return {"message": f"Product {product.title} deleted"}

@app.get("/products/{product_id}/history", response_model=List[PriceLogResponse], tags=["History"])
def get_price_history(product_id: int, limit: int = 100, db: Session = Depends(get_db)):
    """Get price history for a product (for charts/analytics)."""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    history = db.query(PriceLog).filter(PriceLog.product_id == product_id).order_by(PriceLog.timestamp.desc()).limit(limit).all()
    return list(reversed(history))  # Return chronologically

@app.post("/trigger-scan", tags=["Admin"])
def trigger_manual_scan(background_tasks: BackgroundTasks):
    """Force an immediate price check on all tracked items."""
    background_tasks.add_task(check_prices_job)
    return {"message": "✅ Scan triggered - running in background"}

@app.get("/stats", tags=["Admin"])
def get_stats(db: Session = Depends(get_db)):
    """Get system statistics."""
    total_products = db.query(Product).count()
    total_logs = db.query(PriceLog).count()
    
    return {
        "total_products": total_products,
        "total_price_checks": total_logs,
        "database": "SQLite",
        "scheduler": "APScheduler (1-hour interval)"
    }
