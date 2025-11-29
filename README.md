# 🛒 Amazon Price Tracker API

A high-performance **FastAPI** application that concurrently tracks multiple Amazon products, stores history in a relational database (SQLite), and alerts via Email. Features an interactive web dashboard (Swagger UI).

## 🚀 Key Features

* **Multi-Product Support**: Track unlimited products dynamically (no more hardcoded URLs)
* **REST API & Interactive UI**: Full Swagger/OpenAPI documentation at `/docs`
* **Database Persistence**: SQLite with SQLAlchemy ORM keeps permanent price history
* **Background Automation**: APScheduler runs checks every hour without blocking the server
* **Smart Scraping**: Anti-bot headers, CAPTCHA detection, and multiple price selectors
* **Email Alerts**: Instant notifications when prices drop below your target
* **Price Analytics**: Historical data endpoints for charting and analysis

## 🏗 Architecture

```
FastAPI Server (Port 8000)
    ├── REST API Endpoints
    ├── Swagger UI (/docs)
    └── Background Scheduler (APScheduler)
        └── check_prices_job() → runs every 1 hour
            ├── Scrapes all tracked products
            ├── Logs prices to SQLite
            └── Sends email alerts
```

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.9+
- pip (Python package manager)

### 1. Clone & Navigate
```bash
cd price-tracker
```

### 2. Create Virtual Environment (Recommended)
```bash
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
# or
venv\Scripts\activate  # Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Credentials (.env)

Create a `.env` file in the root directory with your Gmail credentials:

```ini
EMAIL_USER=your_email@gmail.com
EMAIL_PASS=your_app_password
EMAIL_RECEIVER=target_email@gmail.com
```

**⚠️ Important:** Use a Gmail **App Password**, not your regular password!
- Go to [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
- Select Mail and Windows Computer
- Copy the 16-character password
- Paste it in `.env` (remove spaces)

## ▶️ Running the Server

```bash
uvicorn src.main:app --reload
```

Output:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
[v] Scheduler started - checks every 1 hour
```

## 📖 Usage Guide

### 1. Open the Interactive Dashboard

Visit: **http://127.0.0.1:8000/docs**

You'll see the Swagger UI with all available endpoints.

### 2. Add a Product (POST /products)

Click **POST /products** → **Try it out** and send:

```json
{
  "title": "iPhone 13 128GB Green",
  "url": "https://www.amazon.in/Apple-iPhone-13-128GB-Green/dp/B09V4B6K53/",
  "target_price": 50000
}
```

Response:
```json
{
  "id": 1,
  "title": "iPhone 13 128GB Green",
  "url": "https://www.amazon.in/Apple-iPhone-13-128GB-Green/dp/B09V4B6K53/",
  "target_price": 50000,
  "last_price": 52990,
  "last_check": "2025-11-29T10:05:00"
}
```

### 3. View All Tracked Products

Click **GET /products** → **Try it out**

Returns list of all products with their current prices.

### 4. Check Price History

Click **GET /products/{product_id}/history** → Enter product ID (e.g., 1)

Returns all historical price points with timestamps - perfect for charting!

### 5. Manual Price Check

Click **POST /trigger-scan** → **Try it out**

Forces an immediate check on all products (doesn't wait for the 1-hour timer).

### 6. Delete a Product

Click **DELETE /products/{product_id}** → Enter product ID

## 📊 Database Structure

Your data is stored in `data/tracker.db`:

**products table:**
```
id | title | url | target_price | last_price | last_check
```

**price_history table:**
```
id | product_id | price | timestamp
```

## 🔍 Troubleshooting

### "CAPTCHA detected - Amazon blocked the request"
- Amazon's anti-bot system temporarily blocked your IP
- Wait 1-2 hours or restart your router/VPN
- The scheduler will keep retrying

### "Could not extract price"
- Amazon's page layout may have changed
- Run `/trigger-scan` and check the `/products/{id}` response
- If it still fails, Amazon may have restructured their HTML

### Email not sending
- Check that credentials in `.env` are correct
- Verify it's an **App Password**, not your regular Gmail password
- Ensure "Less secure app access" is enabled (if using old Gmail)

## 🎯 Next Steps & Enhancement Ideas

### 1. **Telegram/Discord Notifications**
Replace email with instant Telegram/Discord messages:
```python
import requests
webhook_url = "https://discord.com/api/webhooks/..."
requests.post(webhook_url, json={"content": f"Price dropped: ₹{price}"})
```

### 2. **Price Trend Analysis**
Use OpenAI API to analyze historical prices:
```python
import openai
analysis = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": f"Is this a good time to buy? Prices: {history}"}]
)
```

### 3. **Frontend Dashboard**
Create a simple Streamlit/React UI that visualizes price charts:
```bash
pip install streamlit
streamlit run dashboard.py
```

### 4. **Docker Deployment**
Containerize the app for cloud deployment (AWS, Heroku, etc.)

### 5. **Multi-URL Per Product**
Track the same product across multiple sellers and compare prices

## 📝 API Endpoints Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| POST | `/products` | Add a new product |
| GET | `/products` | List all products |
| GET | `/products/{id}` | Get single product |
| DELETE | `/products/{id}` | Remove a product |
| GET | `/products/{id}/history` | Get price history |
| POST | `/trigger-scan` | Force manual price check |
| GET | `/stats` | System statistics |

## 📄 License

Open source - use freely for personal/educational purposes.