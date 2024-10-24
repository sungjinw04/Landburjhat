import random
from datetime import datetime, timedelta
from Lundgrow.database import user_collection, special_user_collection
from Lundgrow import Bot
from Lundgrow.decorators import blacklist_check
from pyrogram import filters
import time

GROW_TIME_LIMIT = 12 * 60 * 60  # 12 hours in seconds

async def get_user_data(user_id, chat_id):
    # Find user and chat-specific data
    user = await user_collection.find_one({"user_id": user_id, "chat_id": chat_id})
    
    if not user:
        # Initialize user data for this chat if not found
        user = {
            "user_id": user_id,
            "chat_id": chat_id,
            "dick_size": 0,
            "last_grow_time": None
        }
        await user_collection.insert_one(user)
    
    return user

async def is_special_user(user_id):
    # Check if user is in the special user list (global check, not per chat)
    return await special_user_collection.find_one({"user_id": user_id}) is not None

async def update_dick_size(user_id, chat_id, new_size):
    # Update the user's dick size and last grow time for the specific chat
    await user_collection.update_one(
        {"user_id": user_id, "chat_id": chat_id},
        {"$set": {"dick_size": new_size, "last_grow_time": datetime.utcnow()}}
    )

@Bot.on_message(filters.command("grow"))
@blacklist_check
async def grow_dick(client, message):
    user_id = message.from_user.id
    chat_id = message.chat.id  # Track by chat ID

    # Fetch user data specific to this chat
    user = await get_user_data(user_id, chat_id)
    dick_size = user["dick_size"]
    last_grow_time = user["last_grow_time"]

    # Check if the user is a special user (bypass time limit for special users)
    if not await is_special_user(user_id):
        if last_grow_time:
            time_since_last_grow = (datetime.utcnow() - last_grow_time).total_seconds()
            if time_since_last_grow < GROW_TIME_LIMIT:
                remaining_time = GROW_TIME_LIMIT - time_since_last_grow
                hours, remainder = divmod(remaining_time, 3600)
                minutes = remainder // 60
                await message.reply(f"You have already played with your dick today.\nNext attempt in {int(hours)}h {int(minutes)}m.")
                return

    # Generate random growth between 1 and 5 cm
    growth = random.randint(1, 5)
    new_dick_size = dick_size + growth

    # Update the user's dick size for this chat
    await update_dick_size(user_id, chat_id, new_dick_size)

    # Send a reply with the updated size
    await message.reply_photo(
        "https://files.catbox.moe/10guiy.jpg",
        caption=f"Your dick has grown by {growth} cm and now it is {new_dick_size} cm long.\nNext attempt in 12h." if not await is_special_user(user_id) else f"Your dick has grown by {growth} cm and now it is {new_dick_size} cm long."
                          )
