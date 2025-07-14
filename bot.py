
import os
import requests
import time
import schedule
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

BASE_URL = "https://visa.vfsglobal.com/ind/en/ita/book-an-appointment"

CENTERS = ["Delhi", "Chandigarh", "Jalandhar"]
KEYWORDS = ["EU Relatives up to 90 days", "Relatives", "90 days"]

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": msg,
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url, data=data)
    except Exception as e:
        print("Failed to send message:", e)

def check_appointments():
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    print("Checking for slots...")
    for city in CENTERS:
        try:
            response = requests.get(BASE_URL, headers=headers)
            soup = BeautifulSoup(response.text, "lxml")
            text = soup.get_text().lower()
            if any(keyword.lower() in text for keyword in KEYWORDS):
                send_telegram(f"✅ *Slot Available* in {city} for EU Relatives (up to 90 days) visa!")
                print(f"Slot found in {city}")
        except Exception as e:
            print(f"Error checking {city}: {e}")

schedule.every(30).seconds.do(check_appointments)

print("Bot started. Checking every 30 seconds...")
while True:
    schedule.run_pending()
    time.sleep(1)
