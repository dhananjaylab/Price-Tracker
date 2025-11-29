# 📚 Documentation Index

Welcome to the Amazon Price Tracker project! Here's a guide to all documentation:

## 🎯 Start Here

1. **[PROJECT_SUMMARY.txt](./PROJECT_SUMMARY.txt)** ← READ THIS FIRST!
   - Complete project overview
   - What's working, what to do next
   - Visual summary of everything

2. **[QUICK_START.md](./QUICK_START.md)** ← Quick reference guide
   - How to run both versions
   - Commands to get started immediately
   - Configuration instructions

## 📖 Detailed Documentation

3. **[README.md](./README.md)** - Full project documentation
   - Architecture overview
   - Installation steps
   - API endpoints reference
   - Feature descriptions

4. **[STATUS.md](./STATUS.md)** - Current project status
   - Both versions tested & working
   - Database structure
   - Data flow diagram
   - Recommendations

5. **[TROUBLESHOOTING.md](./TROUBLESHOOTING.md)** - Problem solving
   - Amazon anti-bot issues
   - Solutions (wait, VPN, Selenium)
   - Testing procedures

## 🔧 Code Files

### Version 1: Simple Script
- **`src/tracker.py`** - Main script
  - Single product tracking
  - CSV logging
  - Email alerts
  - **Status: ✅ TESTED & WORKING**

### Version 2: FastAPI API
- **`src/main.py`** - FastAPI application
  - REST API with 8 endpoints
  - SQLite database
  - Swagger UI dashboard
  - Background scheduler
  - **Status: ✅ READY TO USE**

### Core Components
- **`src/scraper.py`** - Price extraction
  - Anti-bot headers
  - Multiple selectors
  - CAPTCHA detection
  - **Status: ✅ TESTED & WORKING**

- **`src/models.py`** - Database schema
  - Product model
  - PriceLog model

- **`src/__init__.py`** - Package initialization

## ⚙️ Configuration

- **`.env`** - Your Gmail credentials (DO NOT COMMIT)
  - EMAIL_USER
  - EMAIL_PASS (Gmail App Password)
  - EMAIL_RECEIVER

- **`.gitignore`** - Protects sensitive files
  - .env, __pycache__, venv/

- **`requirements.txt`** - Python dependencies
  - fastapi, uvicorn, sqlalchemy, requests, etc.

## 📊 Data

- **`data/price_history.csv`** - V1 data (CSV format)
- **`data/tracker.db`** - V2 data (SQLite database)

## 🧪 Debug Files (Generated during testing)

- `debug_amazon.html` - Amazon page snapshot
- `debug_page.html` - Response debugging
- `page_response.html` - Raw response

## 🚀 How to Use This Project

### For Beginners
1. Read: **PROJECT_SUMMARY.txt**
2. Read: **QUICK_START.md**
3. Run: `python src/tracker.py`

### For Advanced Users
1. Read: **README.md** (full docs)
2. Run: `uvicorn src.main:app --reload`
3. Open: http://127.0.0.1:8000/docs (Swagger UI)

### For Troubleshooting
1. See: **TROUBLESHOOTING.md**
2. Check: **STATUS.md** for architecture

## ✨ Key Features

✅ **Version 1 (Script)**
- Simple, lightweight
- Works with single product
- CSV data logging
- Email alerts
- Automatic scheduling

✅ **Version 2 (API)**
- Multi-product tracking
- REST API endpoints
- Interactive dashboard
- SQLite database
- Real-time history
- Perfect for scaling

## 🎯 Next Steps

1. Choose your version (V1 for simple, V2 for advanced)
2. Update `.env` with Gmail credentials
3. Run the tracker
4. Wait for Amazon to unblock IP if needed
5. View price history and alerts

## 🔗 Useful Links

- FastAPI: https://fastapi.tiangolo.com/
- SQLAlchemy: https://www.sqlalchemy.org/
- BeautifulSoup: https://www.crummy.com/software/BeautifulSoup/

---

**Questions?** Check the relevant documentation file above!

**Happy tracking! 🛍️**
