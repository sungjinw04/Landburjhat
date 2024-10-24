import random
import time
from datetime import datetime, timedelta
from Lundgrow.database import user_collection, special_user_collection
from Lundgrow import Bot
from pyrogram import filters

GROW_TIME_LIMIT = 12 * 60 * 60  

def get_user_data(user_id):
    
    user = user_collection.find_one({"user_id": user_id})
    if not user:
        user = {"user_id": user_id, "dick_size": 0, "last_grow_time": None}
        user_collection.insert_one(user)
    return user

def is_special_user(user_id):
    
    return special_user_collection.find_one({"user_id": user_id}) is not None

def update_dick_size(user_id, new_size):
    
    user_collection.update_one(
        {"user_id": user_id},
        {"$set": {"dick_size": new_size, "last_grow_time": datetime.utcnow()}}
    )

@Bot.on_message(filters.command("grow") & filters.private)
async def grow_dick(client, message):
    user_id = message.from_user.id

    
    user = get_user_data(user_id)
    dick_size = user["dick_size"]
    last_grow_time = user["last_grow_time"]

  
    if not is_special_user(user_id):
        if last_grow_time:
            
            time_since_last_grow = (datetime.utcnow() - last_grow_time).total_seconds()
            
            if time_since_last_grow < GROW_TIME_LIMIT:
                remaining_time = GROW_TIME_LIMIT - time_since_last_grow
                hours, remainder = divmod(remaining_time, 3600)
                minutes = remainder // 60
                await message.reply(f"You have already played with your dick today.\nNext attempt in {int(hours)}h {int(minutes)}m.")
                return

    
    growth = random.randint(1, 5)
    new_dick_size = dick_size + growth

    
    update_dick_size(user_id, new_dick_size)

    
    await message.reply_photo(
        "https://files.catbox.moe/10guiy.jpg",
        caption=f"Your dick has grown by {growth} cm and now it is {new_dick_size} cm long.\nNext attempt in 12h." if not is_special_user(user_id) else f"Your dick has grown by {growth} cm and now it is {new_dick_size} cm long."
    )

