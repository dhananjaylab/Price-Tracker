import os
import csv
import time
import requests
import schedule
import smtplib
import ssl
import random
from datetime import datetime
from bs4 import BeautifulSoup
from email.message import EmailMessage
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class AmazonPriceTracker:
    def __init__(self):
        self.url = os.getenv('TARGET_URL')
        self.target_price = float(os.getenv('TARGET_PRICE', 0))
        self.csv_file = 'data/price_history.csv'
        self.session = requests.Session()
        
        # Hardcoded modern User-Agent often works better than random ones for Amazon
        self.base_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Referer': 'https://www.google.com/',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        
        # Ensure data directory exists
        os.makedirs('data', exist_ok=True)
        if not os.path.exists(self.csv_file):
            with open(self.csv_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Date', 'Time', 'Price'])

    def fetch_price(self):
        """Scrapes Amazon with multi-layer fallback strategies."""
        print(f"[*] Checking price for product...")
        
        # Add random delay to seem human
        time.sleep(random.uniform(1, 3))
        
        try:
            response = self.session.get(self.url, headers=self.base_headers)
            
            if response.status_code != 200:
                print(f"[!] Blocked/Error: HTTP {response.status_code}")
                return None

            soup = BeautifulSoup(response.content, 'html.parser')

            # 1. Check for Bot Detection (CAPTCHA)
            if "Enter the characters you see below" in soup.get_text():
                print("[!] ALERT: Amazon presented a CAPTCHA. IP might be temporarily flagged.")
                self.save_debug_html(soup)
                return None

            # 2. Strategy: Try Multiple Selectors
            price = self.extract_price_logic(soup)
            
            if price:
                return price
            else:
                print("[!] Error: Could not extract price. Layout might have changed.")
                self.save_debug_html(soup)
                return None
                
        except Exception as e:
            print(f"[!] Network Exception: {e}")
            return None

    def extract_price_logic(self, soup):
        """Attempts to find price using different common Amazon patterns."""
        
        # List of potential price containers in order of likelihood
        selectors = [
            # Strategy A: Main price whole number class
            ('span', 'a-price-whole'),
            # Strategy B: Offscreen actual text (often safer)
            ('span', 'a-offscreen'),
            # Strategy C: Deal block price
            ('span', 'apexPriceToPay'),
            # Strategy D: Unified price block
            ('span', 'priceToPay')
        ]

        for tag, class_name in selectors:
            element = soup.find(tag, class_=class_name)
            if element:
                raw_text = element.get_text(strip=True)
                print(f"[*] Found element ({class_name}): {raw_text}")
                
                # Cleanup currency symbols and commas (e.g., "₹70,000.00")
                clean_text = raw_text.replace('₹', '').replace('$', '').replace(',', '')
                
                # Handle cases where offscreen text might be 'Page 1 of 2' or junk
                try:
                    # Extract just the number (float)
                    price = float(clean_text)
                    return price
                except ValueError:
                    continue # Try next selector if text isn't a number
        
        return None

    def save_debug_html(self, soup):
        """Saves HTML to inspect why it failed."""
        with open('debug_fail.html', 'w', encoding='utf-8') as f:
            f.write(str(soup))
        print("[*] Debug: HTML saved to 'debug_fail.html'. Open this file in your browser to check.")

    def log_data(self, price):
        now = datetime.now()
        with open(self.csv_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([now.strftime("%Y-%m-%d"), now.strftime("%H:%M:%S"), price])
        print(f"[{now.strftime('%H:%M:%S')}] Success: Data logged: {price}")

    def send_notification(self, current_price):
        sender_email = os.getenv('EMAIL_USER')
        password = os.getenv('EMAIL_PASS')
        receiver_email = os.getenv('EMAIL_RECEIVER')

        if not sender_email or not password:
            print("[!] Email credentials missing in .env")
            return

        subject = f'🚨 Price Alert: {current_price}'
        body = f"Price dropped to {current_price}! \nLink: {self.url}"

        em = EmailMessage()
        em['From'] = sender_email
        em['To'] = receiver_email
        em['Subject'] = subject
        em.set_content(body)

        context = ssl.create_default_context()
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, em.as_string())
            print("[v] Notification Email Sent!")
        except Exception as e:
            print(f"[!] Email failed: {e}")

    def job(self):
        print("\n--- Starting Cycle ---")
        price = self.fetch_price()
        
        if price:
            self.log_data(price)
            if price <= self.target_price:
                print("[$] Target met! Notifying...")
                self.send_notification(price)
            else:
                print(f"[-] Price {price} is above target {self.target_price}.")
        else:
            print("[!] Skipping this cycle.")

def run_scheduler():
    tracker = AmazonPriceTracker()
    tracker.job() # Run once immediately
    
    # Randomize check time to 60-80 minutes to avoid patterns
    schedule.every(60).to(80).minutes.do(tracker.job)
    
    print("\n[-] Scheduler active (Checks every 60-80 mins). Ctrl+C to stop.")
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    run_scheduler()
