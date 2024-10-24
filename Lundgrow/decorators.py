from functools import wraps
from pyrogram.types import Message
from Lundgrow.database import blacklist_collection  # Assuming you have a collection to store blacklisted chat IDs

def blacklist_check(func):
    @wraps(func)
    async def wrapper(client, message: Message, *args, **kwargs):
        chat_id = message.chat.id
        
        is_blacklisted = await blacklist_collection.find_one({"chat_id": chat_id})

        if is_blacklisted:
            await message.reply_text("This chat is blacklisted and cannot use any commands.")
            return  
        return await func(client, message, *args, **kwargs)
    
    return wrapper
