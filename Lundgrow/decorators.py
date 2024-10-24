from functools import wraps
from pyrogram.types import Message
from Lundgrow.database import blacklist_chats, blacklist_users

def blacklist_chat(func):
    @wraps(func)
    async def wrapper(client, message: Message, *args, **kwargs):
        chat_id = message.chat.id
        
        is_blacklisted = await blacklist_chats.find_one({"chat_id": chat_id})

        if is_blacklisted:
            await message.reply_text("This chat is blacklisted and cannot use any commands.")
            return  
        return await func(client, message, *args, **kwargs)
    
    return wrapper

def blacklist_user(func):
    @wraps(func)
    async def wrapper(client, message, *args, **kwargs):
        user_id = message.from_user.id
        # Check if the user is banned
        banned_user = await blacklist_users.find_one({"user_id": user_id})
        if banned_user:
            await message.reply("You are banned from using this bot.")
            return
        return await func(client, message, *args, **kwargs)
    return wrapper
