import logging
from . import Bot
from .modules import *  # Import all handlers
from pyrogram import idle

# Define the BOTLOG chat ID where you want to send the log
from Lundgrow import BOTLOGS

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def log_imported_modules():
    # Log information about imported modules
    imported_modules = [
        "modules.admin",
        "modules.user",
    ]
    
    for module in imported_modules:
        logger.info(f"Module {module} has been imported successfully.")

async def send_startup_message():
    try:
        await Bot.send_message(BOTLOGS, "Lund Grow Bot has started successfully!")
        logger.info("Startup message sent to BOTLOG.")
    except Exception as e:
        logger.error(f"Failed to send startup message: {e}")

if __name__ == "__main__":
    try:
        log_imported_modules()

        # Start the bot
        Bot.start()
        logger.info("Bot is up and running...")

        # Send a startup message to BOTLOG
        Bot.loop.run_until_complete(send_startup_message())

        # Keep the bot running
        idle()

    except Exception as e:
        logger.error(f"An error occurred: {e}")
    finally:
        Bot.stop()
        logger.info("Bot has stopped.")
