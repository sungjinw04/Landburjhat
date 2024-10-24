import asyncio
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from Lundgrow import Bot
from Lundgrow.database import user_collection
from Lundgrow.config import SUPPORT, SUPPORT_CHANNEL, BOT_USERNAME
from Lundgrow.decorators import blacklist_chat, blacklist_user

@Bot.on_message(filters.command("start") & filters.private)
@blacklist_chat
@blacklist_user
async def start_private(client, message):
    user_id = message.from_user.id
    user_first_name = message.from_user.first_name

    user_data = await user_collection.find_one({"id": user_id})
    if not user_data:
        await user_collection.insert_one({"id": user_id, "details": {"first_name": user_first_name}})
    else:
        if user_data.get("details", {}).get("first_name") != user_first_name:
            await user_collection.update_one(
                {"id": user_id}, 
                {"$set": {"details.first_name": user_first_name}}
            )

    symbols = ["🌟", "❄", "🌈"]
    sent_message = await message.reply_text(symbols[0])

    for symbol in symbols[1:]:
        await asyncio.sleep(1)
        await sent_message.edit_text(symbol)

    await asyncio.sleep(1)
    await sent_message.delete()

    starting_message = await message.reply_text("Starting")
    for i in range(1, 4):
        await asyncio.sleep(1)
        await starting_message.edit_text(f"Starting{'.' * i}")

    await asyncio.sleep(1)
    await starting_message.delete()

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🪭 Add Dick Grower Bot in Your Groups 🪭", url=f'http://t.me/{BOT_USERNAME}?startgroup=new')],
        [InlineKeyboardButton("🏖️ Support 🏖️", url=f'https://t.me/{SUPPORT}'),
         InlineKeyboardButton("🌐 Updates 🌐", url=f'https://t.me/{SUPPORT_CHANNEL}')],
    ])

    await message.reply_photo(
        photo="https://files.catbox.moe/nvni1z.jpg",
        caption=(
            "**I'm a Dick Grower Bot. Become Johnny Sins and surpass him in dick size!**\n\n"
            "Add me to your groups to get started!"
        ),
        reply_markup=keyboard
    )

@Bot.on_message(filters.command("start") & filters.group)
async def start_group(client, message):
    user_id = message.from_user.id
    user_first_name = message.from_user.first_name
    chat_id = message.chat.id

    user_data = await user_collection.find_one({"id": user_id})
    if not user_data:
        await user_collection.insert_one({"id": user_id, "details": {"first_name": user_first_name}})
    else:
        if user_data.get("details", {}).get("first_name") != user_first_name:
            await user_collection.update_one(
                {"id": user_id}, 
                {"$set": {"details.first_name": user_first_name}}
            )

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Contact me in PM", url=f'http://t.me/{BOT_USERNAME}?start=help')]
    ])

    await message.reply_photo(
        photo="https://files.catbox.moe/nvni1z.jpg",
        caption="**If you're looking for information on how to use me, you can always reach out through a private message.**",
        reply_markup=keyboard
    )
