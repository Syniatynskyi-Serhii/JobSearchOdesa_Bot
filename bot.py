import os
import requests
from bs4 import BeautifulSoup

# Отримання даних із секретів GitHub
BOT_TOKEN = os.getenv('BOT_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

# URL для пошуку вакансій у Одесі (Маркетинг)
URL = "https://www.work.ua/jobs-odesa-marketing/"

def get_jobs():
    # Заголовки для імітації реального браузера (вирішує "Помилку запиту до сайту")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "uk-UA,uk;q=0.9,en-US;q=0.8,en;q=0.7"
    }
    
    try:
        response = requests.get(URL, headers=headers, timeout=10)
        if response.status_code != 200:
            print(f"Помилка запиту до сайту. Код відповіді: {response.status_code}")
            return []
    except Exception as e:
        print(f"Помилка підключення: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    jobs = []

    # Парсинг картки вакансій
    cards = soup.find_all('div', class_='job-link')
    
    for card in cards[:5]:  # Беремо перші 5 вакансій
        title_elem = card.find('h2')
        if not title_elem:
            continue
            
        link_elem = title_elem.find('a')
        if not link_elem:
            continue
            
        title = link_elem.text.strip()
        link = "https://www.work.ua" + link_elem['href']
        
        # Отримання назви компанії
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
