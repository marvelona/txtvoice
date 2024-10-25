import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
# Your Telegram bot token from environment variable
TELEGRAM_BOT_TOKEN = os.getenv('7691434356:AAFy5-_KrIxiZJ08xGYvq3iilw5htjZrEPU')

# Function to convert text to audio using Ashlynn TTS API
def ashlynn_tts(text: str) -> str:
    response = requests.get(f'https://ar-tts.ashlynn.workers.dev/?text={text}&type=url')
    if response.status_code == 200:
        return response.json().get('audio')
    return None

# Function to convert text to audio using Google TTS API
def google_tts(text: str, voice: str = 'en-US-Wavenet-C') -> str:
    response = requests.get(f'https://advanced-tts.darkhacker7301.workers.dev/?message={text}&voice={voice}&type=url')
    if response.status_code == 200:
        return response.json().get('audio')
    return None

# Command handler for /tt command (Ashlynn TTS)
async def tt_command(update: Update, context: CallbackContext) -> None:
    if context.args:
        text = ' '.join(context.args)
        audio_url = ashlynn_tts(text)
        if audio_url:
            await update.message.reply_audio(audio=audio_url)
        else:
            await update.message.reply_text("Failed to convert text to audio.")
    else:
        await update.message.reply_text("Please provide text to convert.")

# Command handler for /tG command (Google TTS)
async def tg_command(update: Update, context: CallbackContext) -> None:
    if context.args:
        text = ' '.join(context.args)
        voice = 'en-US-Wavenet-C'  # Default voice, can be customized if needed
        audio_url = google_tts(text, voice)
        if audio_url:
            await update.message.reply_audio(audio=audio_url)
        else:
            await update.message.reply_text("Failed to convert text to audio.")
    else:
        await update.message.reply_text("Please provide text to convert.")

def main() -> None:
    # Create the Application
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Command handlers for TTS
    application.add_handler(CommandHandler('tt', tt_command))  # /tt for Ashlynn TTS
    application.add_handler(CommandHandler('tg', tg_command))  # /tG for Google TTS

    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    main()
