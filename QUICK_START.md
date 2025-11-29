# 🎯 Quick Start Guide - Amazon Price Tracker

## ✅ Both Versions Are Working!

Your tracker has **two fully-functional implementations**. Choose based on your needs:

---

## 🚀 **Quick Start - Version 1 (Recommended for Beginners)**

### Simple Single-Product Tracker

```bash
# Navigate to project
cd price-tracker

# Install dependencies (one-time)
pip install -r requirements.txt

# Run the tracker
python src/tracker.py
```

**What happens:**
- ✅ Checks Amazon price immediately
- ✅ Logs prices to `data/price_history.csv`
- ✅ Sends email alerts when price drops
- ✅ Automatically checks every 60-80 minutes

**To modify tracked product:**
Edit `src/tracker.py` and change the URL/target price.

---

## 🔥 **Advanced - Version 2 (FastAPI Dashboard)**

### Multi-Product Tracker with REST API

```bash
# Install dependencies
pip install -r requirements.txt

# Start the API server
uvicorn src.main:app --reload
```

**Open in browser:**
- Dashboard: **http://127.0.0.1:8000/docs**
- Health check: **http://127.0.0.1:8000/**

**Add products via the dashboard:**
1. Click `POST /products` → Try it out
2. Enter product details:
   ```json
   {
     "title": "iPhone 13",
     "url": "https://www.amazon.in/dp/B09V4B6K53/",
     "target_price": 50000
   }
   ```
3. Submit and watch the price get checked automatically

**API Endpoints:**
- `GET /products` - List all products
- `POST /products` - Add new product
- `GET /products/{id}/history` - View price history
- `POST /trigger-scan` - Force immediate check
- `GET /stats` - View system stats

---

## ⚙️ Configuration (.env)

Create a `.env` file with your Gmail credentials:

```ini
EMAIL_USER=your_email@gmail.com
EMAIL_PASS=your_gmail_app_password
EMAIL_RECEIVER=your_email@gmail.com
```

### Get Gmail App Password:
1. Go to https://myaccount.google.com/apppasswords
2. Select: Mail, Windows Computer
3. Copy the 16-character password
4. Paste into `.env` (remove spaces)

---

## 🛠️ Troubleshooting

### "Could not extract price"
This means **Amazon blocked the request** (normal anti-bot behavior).

**Solutions:**
1. **Wait 1-2 hours** for IP to unblock
2. **Restart router** to get new IP
3. **Use VPN** temporarily
4. See `TROUBLESHOOTING.md` for advanced solutions

### Email not sending
- Verify credentials in `.env` are correct
- Make sure it's an **App Password**, not regular Gmail password
- Check spam folder

---

## 📊 Data Storage

### Version 1 (Script)
- **File:** `data/price_history.csv`
- **Format:** Date, Time, Price
- **Manual check:** Open CSV file

### Version 2 (API)
- **File:** `data/tracker.db` (SQLite)
- **Query via API:** `GET /products/{id}/history`
- **Full price history** with timestamps

---

## 🎓 Project Structure

```
src/
├── tracker.py       ← Run this for simple version
├── main.py          ← Run with uvicorn for API
├── scraper.py       ← Core price extraction logic
├── models.py        ← Database schema
└── __init__.py      ← Package init
```

---

## 💡 Tips

1. **Running in background (Linux/Mac):**
   ```bash
   nohup python src/tracker.py > tracker.log 2>&1 &
   ```

2. **View logs:**
   ```bash
   tail -f tracker.log
   ```

3. **Stop background process:**
   ```bash
   pkill -f "python src/tracker.py"
   ```

4. **Deploy to cloud:**
   - AWS EC2, Heroku, Railway, etc.
   - Use `uvicorn src.main:app` for production
   - Configure database for persistence

---

## 🎯 Which Version Should I Use?

| Feature | V1 Script | V2 API |
|---------|-----------|--------|
| Easy setup | ✅ | ⚠️ |
| Single product | ✅ | ✅ |
| Multiple products | ❌ | ✅ |
| Web dashboard | ❌ | ✅ |
| REST API | ❌ | ✅ |
| Database | CSV | SQLite |
| Background job | ✅ | ✅ |
| Mobile alerts | Email | Email |

**→ Start with V1, upgrade to V2 when needed**

---

## 🔗 Useful Resources

- **Amazon.in Product Links:** https://www.amazon.in/
- **Gmail App Passwords:** https://myaccount.google.com/apppasswords
- **FastAPI Docs:** https://fastapi.tiangolo.com/
- **SQLAlchemy Docs:** https://www.sqlalchemy.org/

---

## 📞 Need Help?

Check the following files:
1. `README.md` - Full documentation
2. `TROUBLESHOOTING.md` - Common issues
3. `STATUS.md` - Current status & architecture

---

**Happy price tracking! 🛍️💰**
