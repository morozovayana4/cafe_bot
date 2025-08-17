# Летняя кафешка — Telegram Bot
Минимальный бот-меню на aiogram 3: добавляешь блюда в корзину, оформляешь заказ — он прилетает владельцу (DEV_CHAT_ID).

## Быстрый старт (через PyCharm тоже ок):
1. Скопируй файлы в папку проекта.
2. Создай виртуальное окружение (PyCharm предложит автоматически) и установи зависимости из `requirements.txt`.
3. Переименуй `.env.example` в `.env` и задай:
   - BOT_TOKEN — новый токен от @BotFather (не публикуй).
   - DEV_CHAT_ID — свой numeric id из @userinfobot.
   - CURRENCY — название валюты.
4. Запусти `bot.py` (Run ▶). В логе появится polling.
5. Открой бота в Telegram и тестируй.

Для продакшена используй любой PaaS (Railway/Render/Fly/Heroku) и запускай `python bot.py`.
