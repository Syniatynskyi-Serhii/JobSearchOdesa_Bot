import os
import requests
from bs4 import BeautifulSoup

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

def send_telegram_message(text):
    if not BOT_TOKEN or not CHAT_ID:
        print("Помилка: Не вказано BOT_TOKEN або CHAT_ID")
        return
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"}
    requests.post(url, data=payload)

def parse_jobs():
    # Пошук вакансій з маркетингу в Одесі на Work.ua
    url = "https://www.work.ua/jobs-odesa-marketing-advertising/"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("Помилка запиту до сайту")
        return

    soup = BeautifulSoup(response.text, "html.parser")
    cards = soup.find_all("div", class_="job-link")

    message = "<b>📊 Нові вакансії з маркетингу в Одесі:</b>\n\n"
    count = 0

    for card in cards[:5]:
        title_elem = card.find("h2")
        if not title_elem:
            continue
        link_elem = title_elem.find("a")
        if not link_elem:
            continue

        title = link_elem.text.strip()
        link = "https://www.work.ua" + link_elem["href"]
        
        message += f"• <b>{title}</b>\n🔗 <a href='{link}'>Переглянути вакансію</a>\n\n"
        count += 1

    if count > 0:
        send_telegram_message(message)
        print(f"Відправлено {count} вакансій.")

if __name__ == "__main__":
    parse_jobs()
