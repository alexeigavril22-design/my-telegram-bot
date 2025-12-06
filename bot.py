import telebot
from telebot import types
import os
from flask import Flask
from threading import Thread
import time
import random

# Получаем токен из переменных окружения
TOKEN = os.getenv('TELEGRAM_TOKEN')
if not TOKEN:
    raise ValueError("❌ ОШИБКА: TELEGRAM_TOKEN не установлен!")
bot = telebot.TeleBot(TOKEN)

# ========== ВСЕ ССЫЛКИ НА ФАЙЛЫ ==========
FILE_URLS = {
    'presentation': 'https://files.catbox.moe/5c5czu.pptx',
    'music1': 'https://files.catbox.moe/gxdo29.mp3',
    'music2': 'https://files.catbox.moe/o67djj.mp3'
}

# ========== ПРОСТОЙ FLASK ДЛЯ KEEP-ALIVE ==========
app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Бот работает! Используйте команду /start в Telegram"

@app.route('/ping')
def ping():
    return 'pong', 200

def run_flask():
    app.run(host='0.0.0.0', port=8080)

# ========== ЗАПУСКАЕМ FLASK В ФОНЕ ==========
Thread(target=run_flask, daemon=True).start()
print("🌐 Flask сервер запущен на порту 8080")

# ========== КЛАВИАТУРЫ ==========
main_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
main_markup.add(
    types.KeyboardButton('📁 Хочу файл'),
    types.KeyboardButton('🎵 Крутая музыка'),
    types.KeyboardButton('📊 Статус бота'),
    types.KeyboardButton('ℹ️ Помощь')
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
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📥 Скачать презентацию", url=url))
    
    bot.send_message(
        message.chat.id,
        '📁 *Презентация готова к скачиванию!*',
        parse_mode='Markdown',
        reply_markup=markup
    )

@bot.message_handler(commands=['music1'])
def send_music1(message):
    bot.send_audio(
        message.chat.id,
        audio=FILE_URLS['music1'],
        title="Khejjter",
        performer="Daryana"
    )

@bot.message_handler(commands=['music2'])
def send_music2(message):
    bot.send_audio(
        message.chat.id,
        audio=FILE_URLS['music2'],
        title="Kto ty",
        performer="Daryana"
    )

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    if message.text == '📁 Хочу файл':
        url = FILE_URLS['presentation']
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("📥 Скачать", url=url))
        bot.send_message(message.chat.id, "Скачайте презентацию:", reply_markup=markup)
    
    elif message.text == '🎵 Крутая музыка':
        bot.send_audio(message.chat.id, audio=FILE_URLS['music1'])
    
    elif message.text == '📊 Статус бота':
        bot.send_message(message.chat.id, "✅ Бот работает отлично! 24/7 режим активен.")
    
    elif message.text == 'ℹ️ Помощь':
        bot.send_message(message.chat.id, "Нажмите /start для начала работы")

# ========== ЗАПУСК БОТА С АВТО-ПЕРЕЗАПУСКОМ ==========
def start_bot():
    print("🤖 Запуск Telegram бота...")
    while True:
        try:
            print("🔄 Бот запущен и слушает сообщения...")
            bot.polling(none_stop=True, interval=1, timeout=30)
        except Exception as e:
            print(f"⚠️ Ошибка: {e}")
            print("🔄 Перезапуск через 5 секунд...")
            time.sleep(5)
            continue

# ========== ГЛАВНЫЙ ЗАПУСК ==========
if __name__ == '__main__':
    print("=" * 60)
    print("🚀 ЗАПУСК ТЕЛЕГРАМ БОТА 24/7")
    print("=" * 60)
    
    # Запускаем бота в отдельном потоке
    bot_thread = Thread(target=start_bot, daemon=True)
    bot_thread.start()
    
    # Бесконечный цикл для главного потока
    try:
        while True:
            time.sleep(60)
            print(f"✅ Бот активен: {time.strftime('%H:%M:%S')}")
    except KeyboardInterrupt:
        print("\n🛑 Остановка...")
