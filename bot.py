import os
import requests

BOT_TOKEN = os.getenv('BOT_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

# Публічний API Robota.ua (Одеса = cityId 2, Маркетинг = rubricId 14)
API_URL = "https://api.rabota.ua/vacancy/search"

def get_jobs():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    
    payload = {
        "cityId": 2,        # Одеса
        "rubricId": 14,     # Маркетинг / Реклама / PR
        "pageSize": 5
    }
    
    try:
        response = requests.get(API_URL, params=payload, headers=headers, timeout=10)
        if response.status_code != 200:
            print(f"Помилка Robota.ua API: Код {response.status_code}")
            return []
            
        data = response.json()
        documents = data.get('documents', [])
        
        jobs = []
        for doc in documents:
            title = doc.get('name', 'Без назви')
            vacancy_id = doc.get('id')
            company = doc.get('companyName', 'Компанія не вказана')
            link = f"https://robota.ua/company{doc.get('companyId', 0)}/vacancy{vacancy_id}"
            
            jobs.append(f"<b>{title}</b>\n<i>{company}</i>\n<a href='{link}'>Переглянути вакансію</a>")
            
        return jobs
    except Exception as e:
        print(f"Помилка підключення: {e}")
        return []

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
        message = "<b>🚀 Топ-5 нових вакансій з Robota.ua (Маркетинг, Одеса):</b>\n\n" + "\n\n".join(job_list)
        send_telegram(message)
        print("Вакансії успішно надіслано в Telegram.")
    else:
        print("Вакансій не знайдено або сталася помилка.")
