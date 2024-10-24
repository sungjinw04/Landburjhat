import logging
from . import Bot
from .modules import * # Import all handlers
from pyrogram import idle

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

if __name__ == "__main__":
    try:
        
        log_imported_modules()

        
        Bot.start()
        logger.info("Bot is up and running...")

        
        idle()

    except Exception as e:
        logger.error(f"An error occurred: {e}")
    finally:
        
        Bot.stop()
        logger.info("Bot has stopped.")
