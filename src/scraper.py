import re
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

ua = UserAgent()

def fetch_amazon_price(url: str):
    """Fetch Amazon product price with anti-bot headers and multiple fallback selectors."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://www.google.com/',
        'Upgrade-Insecure-Requests': '1',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Cache-Control': 'max-age=0',
    }

    try:
        session = requests.Session()
        response = session.get(url, headers=headers, timeout=15)

        if response.status_code != 200:
            print(f"[!] Error {response.status_code} for {url}")
            return None

        # Check if response is suspiciously small (likely blocked)
        if len(response.content) < 10000:
            if '₹' not in response.text:
                print(f"[!] WARNING: Amazon may have blocked this request")
                return None

        soup = BeautifulSoup(response.content, 'html.parser')

        # Check for block messages
        if any(msg in soup.get_text() for msg in ["Enter the characters", "Please try again", "robot"]):
            print("[!] CAPTCHA or block detected")
            return None

        # Strategies for price extraction (in priority order)
        selectors = [
            ('span', 'a-price-whole'),
            ('span', 'a-offscreen'),
            ('span', 'priceToPay'),
            ('span', 'apexPriceToPay'),
        ]

        for tag, cls in selectors:
            elem = soup.find(tag, class_=cls)
            if elem:
                txt = elem.get_text(strip=True)
                txt = txt.replace('₹', '').replace('$', '').replace(',', '').replace('.', '').strip()
                numbers = re.findall(r'\d+', txt)

                if numbers:
                    try:
                        price_str = numbers[0]
                        price = float(price_str)
                        if price > 100:
                            return price
                    except (ValueError, IndexError):
                        continue

        print(f"[!] Could not extract price from {url}")
        return None

    except requests.exceptions.RequestException as e:
        print(f"[!] Network error: {e}")
        return None
    except Exception as e:
        print(f"[!] Scrape failed: {e}")
        return None
