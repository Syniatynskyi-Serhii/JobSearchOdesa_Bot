import os
import requests
import feedparser

BOT_TOKEN = os.getenv('BOT_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

# RSS-стрічка Work.ua для категорії "Маркетинг, реклама, PR" в Одесі
RSS_URL = "https://www.work.ua/rss/odesa-marketing/"

def get_jobs():
    try:
       feed = feedparser.parse(
    RSS_URL,
    agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
)
            
        jobs = []
        for entry in feed.entries[:5]:  # Беремо 5 останніх вакансій
            title = entry.title
            link = entry.link
            
            jobs.append(f"<b>{title}</b>\n<a href='{link}'>Переглянути вакансію</a>")
            
        return jobs
    except Exception as e:
        print(f"Помилка читання RSS: {e}")
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
        message = "<b>🚀 Топ-5 нових вакансій (Маркетинг, Одеса):</b>\n\n" + "\n\n".join(job_list)
        send_telegram(message)
        print("Вакансії успішно надіслано в Telegram.")
    else:
        print("Вакансій не знайдено або сталася помилка.")
