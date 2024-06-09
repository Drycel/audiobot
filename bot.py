import os
from pytube import YouTube
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from dotenv import load_dotenv

# Завантаження змінних середовища з .env файлу
load_dotenv()

# Ваш Telegram токен
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

# Переконайтеся, що токен завантажено
if not TELEGRAM_TOKEN:
    print("Помилка: Токен не знайдено у файлі .env")
    exit(1)
else:
    print("Токен успішно завантажено")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Привіт! Надішліть мені посилання на YouTube відео, і я надішлю вам аудіо!')

async def download_audio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    url = update.message.text
    await update.message.reply_text('Завантаження аудіо, будь ласка, зачекайте...')

    try:
        # Завантаження аудіо з YouTube
        yt = YouTube(url)
        stream = yt.streams.filter(only_audio=True).first()
        audio_file = stream.download()

        # Надсилання аудіо в Telegram
        with open(audio_file, 'rb') as audio:
            await context.bot.send_audio(chat_id=update.message.chat_id, audio=audio)
        os.remove(audio_file)
    except Exception as e:
        await update.message.reply_text(f'Сталася помилка: {e}')

def main() -> None:
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_audio))

    application.run_polling()

if __name__ == '__main__':
    main()

