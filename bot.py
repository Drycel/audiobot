import os
from pytube import YouTube
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Завантаження змінних середовища з файлу .env
load_dotenv()

# Ваш Telegram токен
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

# Переконайтеся, що токен завантажено
if not TELEGRAM_TOKEN:
    logger.error("Помилка: Токен не знайдено у файлі .env")
    exit(1)
else:
    logger.info(f"Токен успішно завантажено: {TELEGRAM_TOKEN}")

def start(update: Update, context: CallbackContext) -> None:
    logger.info("Виклик функції start")
    update.message.reply_text('Привіт! Надішліть мені посилання на YouTube відео, і я надішлю вам аудіо!')

def download_audio(update: Update, context: CallbackContext) -> None:
    url = update.message.text
    logger.info(f"Отримано URL: {url}")
    update.message.reply_text('Завантаження аудіо, будь ласка, зачекайте...')

    try:
        # Завантаження аудіо з YouTube
        yt = YouTube(url)
        stream = yt.streams.filter(only_audio=True).first()
        audio_file = stream.download()

        # Надсилання аудіо в Telegram
        context.bot.send_audio(chat_id=update.message.chat_id, audio=open(audio_file, 'rb'))
        os.remove(audio_file)
    except Exception as e:
        logger.error(f'Сталася помилка: {e}')
        update.message.reply_text(f'Сталася помилка: {e}')

def main() -> None:
    logger.info("Запуск бота")
    updater = Updater(TELEGRAM_TOKEN, use_context=True)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, download_audio))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

