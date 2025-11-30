import logging
import asyncio
import os
import random
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import FSInputFile
from aiogram.exceptions import TelegramForbiddenError, TelegramRetryAfter

# Load API Token from environment variable
API_TOKEN = ""  # Replace with your bot token
TARGET_USER_ID = []
MUSIC_FOLDER = r"/Users/tatipoki/Downloads/"
# Setup logging (log to both file and console)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler("chat_log.txt"),
        logging.StreamHandler()
    ]
)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

async def send_random_song(user_id: int):
    """Send a random MP3 file from the music folder."""
    try:
        mp3_files = [f for f in os.listdir(MUSIC_FOLDER) if f.endswith(".mp3")]
        mp4_files = [f for f in os.listdir(MUSIC_FOLDER) if f.endswith(".mp4")]
        all = [f for f in mp3_files or mp4_files]
        if not all:
            await bot.send_message(user_id, "No songs available right now.")
            logging.warning(f"No songs found in {MUSIC_FOLDER}")
            return

        song_file = random.choice(all)
        song_path = os.path.join(MUSIC_FOLDER, song_file)
        if(song_file.endswith(".mp3")) :
            await bot.send_audio(
                user_id,
                FSInputFile(song_path),
                caption=f" 🍫 🍫 🍫 "
            )
        else :
            await bot.send_video(
                user_id,
                FSInputFile(song_path),
                caption=f" sorry"
            )
        logging.info(f"Sent song {song_file} to user {user_id}")
        
    except TelegramRetryAfter as e:
        logging.warning(f"Rate limit hit. Retrying in {e.retry_after} seconds...")
        await asyncio.sleep(e.retry_after)
        await send_random_song(user_id)  # Retry after delay
    except TelegramForbiddenError:
        logging.error(f"Cannot send message to user {user_id} (blocked or disabled messages).")
    except Exception as e:
        logging.error(f"Error sending song: {e}")

async def send_initial_hi():
    """Send a 'Hi' message to the target user when the bot starts."""
    try:
        await bot.send_message(TARGET_USER_ID, "Hi! ðŸŽµ Send me a '1'")
        logging.info(f"Sent initial 'Hi' message to user {TARGET_USER_ID}")
    except TelegramForbiddenError:
        logging.error(f"Cannot message user {TARGET_USER_ID} (blocked bot).")
    except Exception as e:
        logging.error(f"Failed to send initial message: {e}")
@dp.message(Command("start"))
async def start_command(message: types.Message):
    """Handle /start command."""
    user_id = message.from_user.id
    username = message.from_user.username or "NoUsername"
    logging.info(f"User {username} (ID: {user_id}) issued /start command")

    if user_id in TARGET_USER_ID:  # âœ… Corrected
        await message.answer("Hi again! ðŸŽµ Send me a '1' again!")
    else:
        await message.answer("Hello! This bot is for authorized users only.")
        logging.warning(f"Unauthorized access attempt by {username} (ID: {user_id})")

async def send_initial_hi():
    """Send a 'Hi' message to the target users when the bot starts."""
    for user_id in TARGET_USER_ID:
        try:
            await bot.send_message(user_id, "Hi! ðŸŽµ Send me a '1'")
            logging.info(f"Sent initial 'Hi' message to user {user_id}")
        except TelegramForbiddenError:
            logging.error(f"Cannot message user {user_id} (blocked bot).")
        except Exception as e:
            logging.error(f"Failed to send initial message to {user_id}: {e}")

@dp.message()
async def handle_message(message: types.Message):
    """Handle incoming messages."""
    user_id = message.from_user.id
    username = message.from_user.username or "NoUsername"
    logging.info(f"User {username} (ID: {user_id}) sent: {message.text}")

    if user_id in TARGET_USER_ID:  # âœ… Fixed condition
        if message.text.strip() == "1":
            await send_random_song(user_id)
        else:
            await message.answer("Please send '1' to receive a random song!")
    else:
        await message.answer("You are not authorized to use this bot.")
        logging.warning(f"Unauthorized user {username} (ID: {user_id}) attempted interaction.")

async def main():
    """Main function to start the bot."""
    try:
        # Send initial "Hi" message when bot starts
        # Start polling
        await dp.start_polling(bot)
    except Exception as e:
        logging.error(f"Bot encountered an error: {e}")
    finally:
        await bot.session.close()  # Properly close bot session
        logging.info("Bot has been shut down.")

if __name__ == "__main__":
    # Ensure the music folder exists
    if not os.path.exists(MUSIC_FOLDER):
        os.makedirs(MUSIC_FOLDER)
        logging.warning(f"Created missing music folder: {MUSIC_FOLDER}")
    
    # Run the bot
    logging.info("Starting the bot...")
    asyncio.run(main())
