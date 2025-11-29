# 🛒 Amazon Price Tracker

A robust Python application that monitors Amazon product prices, logs historical data, and sends email notifications when prices drop below a specified threshold.

## 🏗 Architecture

The system follows a modular pipeline design:
1. **Scheduler:** Trigger checking jobs at defined intervals.
2. **Scraper:** Fetches raw HTML using rotating User-Agents to mimic real browsers.
3. **Parser:** Extracts specific pricing information.
4. **Data Layer:** Persists price history to a local CSV store.
5. **Notifier:** Sends email alerts securely when conditions are met.

*(Refer to project diagram for visual flow)*

## 🚀 Features

* **Secure:** Credentials managed via Environment Variables.
* **Stealthy:** Uses fake User-Agents to prevent bot detection.
* **Persistent:** Logs every check to `data/price_history.csv` for analysis.
* **Automated:** Runs on a continuous loop via a built-in scheduler.

## 🛠️ Setup & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/dhananjaylab/price-tracker.git
cd price-tracker
```

### 2. Create Virtual Environment (Recommended)

```bash
# Mac/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configuration (.env)

Create a `.env` file in the root directory. Copy the following and fill in your details:

**Note:** For Gmail, you must use an **App Password**, not your login password.

```ini
EMAIL_USER=your_email@gmail.com
EMAIL_PASS=your_gmail_app_password
EMAIL_RECEIVER=receiver_email@gmail.com
TARGET_URL=https://www.amazon.in/dp/YOUR_PRODUCT_ID
TARGET_PRICE=70000
```

## ▶️ How to Run

Run the application:

```bash
python src/tracker.py
```

The script will:

- Check the price immediately.
- Create a CSV file in the `data/` folder if it doesn't exist.
- Enter a sleep loop and check again every hour (configurable in `src/tracker.py`).

## 📊 Data Output

Prices are logged in the following format in `data/price_history.csv`:

```csv
Date,Time,Price
2023-10-25,14:00:01,72000.0
2023-10-25,15:00:01,71500.0
```

## 🔐 Security Notes

- **Never commit `.env` file** - It's already in `.gitignore`
- Use Gmail App Passwords for authentication (not your main password)
- Rotate credentials periodically if needed

## 📝 License

This project is open source and available under the MIT License.