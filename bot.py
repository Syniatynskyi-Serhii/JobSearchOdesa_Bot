import os
import sys

# Зчитуємо токен із змінних середовища (GitHub Secrets)
BOT_TOKEN = os.environ.get("BOT_TOKEN")

# Перевірка наявності токена
if not BOT_TOKEN:
    print("Помилка: Токен 'BOT_TOKEN' не знайдено в змінних середовища!")
    sys.exit(1)

print("Успіх: Токен успішно зчитано!")
