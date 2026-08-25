import os
import requests

BOT_TOKEN = os.getenv('BOT_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

API_URL = "https://api.rabota.ua/vacancy/search"

def get_jobs():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    
    # Використовуємо точний текстовий пошук замість rubricId
    payload = {
        "keyWords": "маркетинг",
        "cityId": 2,          # ID Одеси
        "pageSize": 20,       # Беремо запас для подальшої фільтрації
        "page": 1
    }
    
    try:
        response = requests.get(API_URL, params=payload, headers=headers, timeout=10)
        if response.status_code != 200:
            print(f"Помилка API: {response.status_code}")
            return []
            
        data = response.json()
        documents = data.get('documents', [])
        
        jobs = []
        for doc in documents:
            cityName = doc.get('cityName', '')
            
            # Жорсткий фільтр за містом (пропускаємо все, що не Одеса)
            if "Одеса" not in cityName and "Odesa" not in cityName:
                continue
                
            title = doc.get('name', 'Без назви')
            vacancy_id = doc.get('id')
            company = doc.get('companyName', 'Компанія не вказана')
            link = f"https://robota.ua/company{doc.get('companyId', 0)}/vacancy{vacancy_id}"
            
            jobs.append(f"<b>{title}</b> (Одеса)\n<i>{company}</i>\n<a href='{link}'>Переглянути вакансію</a>")
            
            # Зупиняємо збір, коли сформовано 5 відповідних вакансій
            if len(jobs) == 5:
                break
            
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
    
    requests.post(url, json=payload)

if __name__ == "__main__":
    job_list = get_jobs()
    
    if job_list:
        message = "<b>🚀 Топ-5 точних вакансій (Маркетинг, Одеса):</b>\n\n" + "\n\n".join(job_list)
        send_telegram(message)
        print("Вакансії успішно надіслано в Telegram.")
    else:
        print("Відповідних вакансій не знайдено.")
