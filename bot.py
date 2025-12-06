import telebot
from telebot import types
import os
from flask import Flask
from threading import Thread
import time
import random
from keep_alive import start_keep_alive, start_auto_ping
import requests

# Узнаем наш URL
repl_owner = os.environ.get('REPL_OWNER', 'alexeigavril22')
repl_slug = os.environ.get('REPL_SLUG', 'telegram-bot-24-7')

print("=" * 60)
print("🌐 ВАШ URL ДЛЯ БОТА:")
print("=" * 60)
print(f"https://{repl_slug}.{repl_owner}.repl.co")
print("=" * 60)
print("📌 Добавьте /ping в конце для проверки:")
print(f"https://{repl_slug}.{repl_owner}.repl.co/ping")
print("=" * 60)

TOKEN = os.getenv('TELEGRAM_TOKEN')
if not TOKEN:
    raise ValueError("TELEGRAM_TOKEN environment variable is required. Please set it in your secrets.")
bot = telebot.TeleBot(TOKEN)

# ========== ВСЕ ССЫЛКИ НА ФАЙЛЫ ==========
FILE_URLS = {
    'presentation': 'https://files.catbox.moe/5c5czu.pptx',
    'music1': 'https://files.catbox.moe/gxdo29.mp3',     # первая музыка
    'music2': 'https://files.catbox.moe/o67djj.mp3'      # вторая музыка
}

# ========== FLASK ДЛЯ 24/7 ==========
app = Flask(__name__)

@app.route('/')
def home():
    return """
    <html>
    <head>
        <title>🤖 Telegram Bot 24/7</title>
        <meta http-equiv="refresh" content="30">
        <style>
            body { 
                font-family: 'Segoe UI', Arial, sans-serif; 
                text-align: center; 
                padding: 40px; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                min-height: 100vh;
                margin: 0;
            }
            .container {
                background: rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(10px);
                padding: 40px;
                border-radius: 20px;
                display: inline-block;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                border: 1px solid rgba(255,255,255,0.2);
            }
            h1 { 
                font-size: 2.5em; 
                margin-bottom: 20px;
                text-shadow: 0 2px 10px rgba(0,0,0,0.3);
            }
            .status {
                background: #4CAF50;
                padding: 12px 25px;
                border-radius: 30px;
                display: inline-block;
                margin: 20px 0;
                font-weight: bold;
                font-size: 1.2em;
            }
            .links {
                margin-top: 30px;
                text-align: left;
                display: inline-block;
            }
            .link-item {
                background: rgba(255,255,255,0.1);
                padding: 15px;
                margin: 10px 0;
                border-radius: 10px;
                border-left: 4px solid #4CAF50;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🤖 Telegram Bot 24/7</h1>
            <div class="status">✅ АКТИВЕН И РАБОТАЕТ</div>
            <p>Бот с презентацией и музыкой доступен в Telegram</p>

            <div class="links">
                <div class="link-item">
                    <strong>📁 Презентация:</strong> Готова к скачиванию
                </div>
                <div class="link-item">
                    <strong>🎵 Музыка 1:</strong> Khejjter
                </div>
                <div class="link-item">
                    <strong>🎵 Музыка 2:</strong> Kto ty
                </div>
            </div>

            <p style="margin-top: 30px;">
                <a href="/ping" style="color: #FFD700; text-decoration: none; font-weight: bold;">
                    🔗 Проверить статус (/ping)
                </a>
            </p>
        </div>
    </body>
    </html>
    """

@app.route('/ping')
def ping():
    return 'OK', 200

def run_flask():
    app.run(host='0.0.0.0', port=5000)

# ========== КЛАВИАТУРЫ ==========
main_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
main_markup.add(
    types.KeyboardButton('📁 Хочу файл'),
    types.KeyboardButton('🎵 Крутая музыка'),
    types.KeyboardButton('📊 Статус бота'),
    types.KeyboardButton('ℹ️ Помощь')
)

music_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
music_markup.add(
    types.KeyboardButton('🎵 Дополнительная музыка'),
    types.KeyboardButton('🎵 Повторить музыку'),
    types.KeyboardButton('🔙 Назад в меню'),
    types.KeyboardButton('📁 Хочу файл')
)

# ========== КОМАНДЫ БОТА ==========
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        '👋 *Привет! Я твой бот работающий 24/7!*\n\n'
        '✨ *Что я умею:*\n'
        '• 📁 Отправлять презентацию "Жизнь и творчество И.А. Бунина"\n'
        '• 🎵 Отправлять крутую музыку (2 трека)\n'
        '• ⏰ Работать круглосуточно без перерывов\n\n'
        '📌 *Используй кнопки ниже или команды:*\n'
        '/presentation - получить презентацию\n'
        '/music1 - первая музыка\n'
        '/music2 - вторая музыка\n'
        '/status - проверить работу',
        parse_mode='Markdown',
        reply_markup=main_markup
    )

@bot.message_handler(commands=['presentation'])
def send_presentation(message):
    url = FILE_URLS['presentation']

    # Инлайн кнопки
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("📥 Скачать файл", url=url),
        types.InlineKeyboardButton("👁️ Посмотреть онлайн", 
            url="https://files.catbox.moe/5c5czu.pptx")
    )

    bot.send_message(
        message.chat.id,
        '📊 *Презентация: "Жизнь и творчество И.А. Бунина"*\n\n'
        '✅ *Файл готов к скачиванию!*\n\n'
        'Выберите вариант получения:',
        parse_mode='Markdown',
        reply_markup=markup
    )

@bot.message_handler(commands=['music1'])
def send_music1(message):
    url = FILE_URLS['music1']

    bot.send_audio(
        message.chat.id,
        audio=url,
        title="Khejjter",
        performer="Daryana",
        reply_markup=music_markup
    )

    bot.send_message(
        message.chat.id,
        '🎵 *Первая музыка отправлена!*\n\n'
        'Хотите дополнительную музыку или вернуться в меню?',
        parse_mode='Markdown',
        reply_markup=music_markup
    )

@bot.message_handler(commands=['music2'])
def send_music2(message):
    url = FILE_URLS['music2']

    bot.send_audio(
        message.chat.id,
        audio=url,
        title="Kto ty",
        performer="Daryana",
        reply_markup=music_markup
    )

    bot.send_message(
        message.chat.id,
        '🎶 *Вторая музыка отправлена!*',
        parse_mode='Markdown',
        reply_markup=music_markup
    )

@bot.message_handler(commands=['status', 'info'])
def status_cmd(message):
    bot.send_message(
        message.chat.id,
        '📊 *Статус бота:*\n\n'
        '✅ *Состояние:* АКТИВЕН\n'
        '⏰ *Режим:* 24/7 (круглосуточно)\n'
        '📍 *Хостинг:* Replit Cloud\n'
        '🔄 *Автовосстановление:* ВКЛЮЧЕНО\n\n'
        '📁 *Доступные файлы:*\n'
        '• Презентация (.pptx) - 1 файл\n'
        '• Музыка (.mp3) - 2 трека\n\n'
        '🤖 Бот готов к работе!',
        parse_mode='Markdown',
        reply_markup=main_markup
    )

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    text = message.text

    if text == '📁 Хочу файл':
        url = FILE_URLS['presentation']

        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton("📥 Скачать презентацию", url=url)
        )

        bot.send_message(
            message.chat.id,
            '📁 *Отправляю презентацию...*\n\n'
            '🎯 *Название:* Жизнь и творчество И.А. Бунина\n'
            '📊 *Формат:* PowerPoint (PPTX)\n'
            '💾 *Размер:* ~1-5 МБ\n\n'
            '✅ *Файл готов к скачиванию!*\n'
            'Нажмите кнопку ниже:',
            parse_mode='Markdown',
            reply_markup=markup
        )

        bot.send_message(
            message.chat.id,
            f'🔗 *Прямая ссылка:*\n`{url}`\n\n'
            '_Скопируйте если кнопка не работает_',
            parse_mode='Markdown',
            reply_markup=main_markup
        )

    elif text == '🎵 Крутая музыка':
        url = FILE_URLS['music1']

        bot.send_audio(
            message.chat.id,
            audio=url,
            title="Khejjter",
            performer="Daryana",
            duration=180  # примерная длительность
        )

        bot.send_message(
            message.chat.id,
            '🎵 *Первая музыка: "Khejjter"*\n'
            '👤 *Исполнитель:* Daryana\n\n'
            'Хотите дополнительную музыку?',
            parse_mode='Markdown',
            reply_markup=music_markup
        )

    elif text == '🎵 Дополнительная музыка':
        url = FILE_URLS['music2']

        bot.send_audio(
            message.chat.id,
            audio=url,
            title="Kto ty",
            performer="Daryana"
        )

        bot.send_message(
            message.chat.id,
            '🎶 *Вторая музыка: "Kto ty"*\n'
            '👤 *Исполнитель:* Daryana\n\n'
            'Что дальше?',
            parse_mode='Markdown',
            reply_markup=music_markup
        )

    elif text == '🎵 Повторить музыку':
        # Повторно отправляем первую музыку
        url = FILE_URLS['music1']
        bot.send_audio(message.chat.id, audio=url, title="Khejjter", performer="Daryana")
        bot.send_message(message.chat.id, '🎵 Повторяю первую музыку!', reply_markup=music_markup)

    elif text == '📊 Статус бота':
        bot.send_message(
            message.chat.id,
            '🤖 *Бот работает исправно!*\n\n'
            'Все функции доступны:\n'
            '✅ Презентация\n'
            '✅ 2 трека музыки\n'
            '✅ Круглосуточная работа\n\n'
            'Используйте кнопки для навигации!',
            parse_mode='Markdown',
            reply_markup=main_markup
        )

    elif text == 'ℹ️ Помощь':
        bot.send_message(
            message.chat.id,
            '📚 *Доступные команды:*\n\n'
            '*/start* - начать работу\n'
            '*/presentation* - получить презентацию\n'
            '*/music1* - первая музыка (Khejjter)\n'
            '*/music2* - вторая музыка (Kto ty)\n'
            '*/status* - статус бота\n\n'
            '📌 *Или используйте кнопки:*\n'
            '📁 Хочу файл - презентация\n'
            '🎵 Крутая музыка - первый трек\n'
            '🎵 Дополнительная музыка - второй трек\n'
            '🔙 Назад в меню - вернуться',
            parse_mode='Markdown',
            reply_markup=main_markup
        )

    elif text == '🔙 Назад в меню':
        bot.send_message(
            message.chat.id,
            '🔙 *Возвращаю в главное меню!*\n\n'
            'Выберите действие:',
            parse_mode='Markdown',
            reply_markup=main_markup
        )

    else:
        bot.reply_to(message, message.text, reply_markup=main_markup)
        responses = [
            f"Вы написали: {message.text}",
            f"Эхо: {message.text}",
            f"Повторяю: {message.text}",
            f"Сообщение получено: {message.text}"
        ]
        bot.send_message(message.chat.id, random.choice(responses), reply_markup=main_markup)
# ========== ЗАПУСК ==========
if __name__ == '__main__':
    print("=" * 70)
    print("🚀 ТЕЛЕГРАМ БОТ ЗАПУЩЕН С АВТО-ВОССТАНОВЛЕНИЕМ 24/7")
    print("=" * 70)

    # Запускаем keep-alive систему
    keep_alive_thread = start_keep_alive()
    ping_thread = start_auto_ping()

    # Запускаем Flask для UptimeRobot
    Thread(target=run_flask, daemon=True).start()
    time.sleep(2)

    print("✅ ВСЕ СИСТЕМЫ ЗАПУЩЕНЫ:")
    print("  1. Keep-alive сервер (порт 8080)")
    print("  2. Авто-пинг (каждые 5 минут)")
    print("  3. Flask сервер (порт 5000)")
    print("  4. Telegram бот")
    print("=" * 70)

    # Функция для авто-перезапуска при ошибках
    def restart_on_error():
        """Перезапускает бота при ошибках"""
        while True:
            try:
                bot.polling(non_stop=True, interval=1, timeout=30)
            except Exception as e:
                print(f"⚠️ Ошибка бота: {e}")
                print("🔄 Перезапуск через 10 секунд...")
                time.sleep(10)
                continue

    # Запускаем бота с авто-перезапуском
    bot_thread = Thread(target=restart_on_error, daemon=True)
    bot_thread.start()

    print("🤖 Бот запущен с авто-перезапуском при ошибках")
    print("=" * 70)

    # Бесконечный цикл для главного потока
    try:
        while True:
            time.sleep(60)
            print("⏰ Бот активен...", time.strftime("%Y-%m-%d %H:%M:%S"))
    except KeyboardInterrupt:
        print("\n🛑 Остановка бота...")
