import os
import requests
import cloudscraper
from bs4 import BeautifulSoup

BOT_TOKEN = os.getenv('BOT_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

URL = "https://www.work.ua/jobs-odesa-marketing/"

def get_jobs():
    # Створення скрапера для обходу Cloudflare / 403 Forbidden
    scraper = cloudscraper.create_scraper(
        browser={
            'browser': 'chrome',
            'platform': 'windows',
            'desktop': True
        }
    )

    try:
        response = scraper.get(URL, timeout=15)
        if response.status_code != 200:
            print(f"Помилка запиту до сайту. Код відповіді: {response.status_code}")
            return []
    except Exception as e:
        print(f"Помилка підключення: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    jobs = []

    cards = soup.find_all('div', class_='job-link')

    for card in cards[:5]:
        title_elem = card.find('h2')
        if not title_elem:
            continue

        link_elem = title_elem.find('a')
        if not link_elem:
            continue

        title = link_elem.text.strip()
        link = "https://www.work.ua" + link_elem['href']

        company_elem = card.find('div', class_='add-top-xs')
        company = company_elem.text.strip() if company_elem else "Компанію не вказано"

        jobs.append(f"<b>{title}</b>\n<i>{company}</i>\n<a href='{link}'>Переглянути вакансію</a>")

    return jobs

def send_telegram(text):
    if not BOT_TOKEN or not CHAT_ID:
        print("Помилка: Відсутній BOT_TOKEN або CHAT_ID")
        return

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": False
    }

    res = requests.post(url, json=payload)
    if res.status_code != 200:
        print(f"Помилка надсилання в Telegram: {res.text}")

if __name__ == "__main__":
    job_list = get_jobs()

    if job_list:
        message = "<b>🚀 Топ-5 нових вакансій (Маркетинг, Одеса):</b>\n\n" + "\n\n".join(job_list)
        send_telegram(message)
        print("Вакансії успішно надіслано в Telegram.")
    else:
        print("Вакансій не знайдено або сталася помилка.")
