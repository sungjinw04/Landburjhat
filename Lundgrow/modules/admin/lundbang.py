from pyrogram import filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from Lundgrow import Bot
from Lundgrow.database import blacklist_users
from ...config import OWNER_ID, DEV_ID

@Bot.on_message(filters.command("lundbang") & filters.reply)
async def bang_user(client, message):
    if int(message.from_user.id) not in DEV_ID and int(message.from_user.id) not in OWNER_ID:
        await message.reply("You are not authorized to use this command.")
        return

    try:
        # Get the user_id from the replied message
        user_id = message.reply_to_message.from_user.id
        first_name = message.reply_to_message.from_user.first_name

        # Check if the user is already banned
        existing = await blacklist_users.find_one({"user_id": user_id})
        if existing:
            await message.reply(f"{first_name} is already banged.")
            return

        # Insert the user_id into the blacklist_user collection
        await blacklist_users.insert_one({"user_id": user_id, "first_name": first_name})

        await message.reply(f"Successfully lund banged [{first_name}](tg://user?id={user_id})", parse_mode=enums.ParseMode.MARKDOWN)

    except Exception as e:
        await message.reply(f"An error occurred: {str(e)}")


@Bot.on_message(filters.command("unlundbang") & filters.reply)
async def unbang_user(client, message):
    if int(message.from_user.id) not in DEV_ID and int(message.from_user.id) not in OWNER_ID:
        await message.reply("You are not authorized to use this command.")
        return

    try:
        # Get the user_id from the replied message
        user_id = message.reply_to_message.from_user.id
        first_name = message.reply_to_message.from_user.first_name

        # Check if the user is in the blacklist
        existing = await blacklist_users.find_one({"user_id": user_id})
        if not existing:
            await message.reply(f"{first_name} is not banged.")
            return

        # Remove the user from the blacklist
        await blacklist_users.delete_one({"user_id": user_id})

        await message.reply(f"Successfully un-lundbanged [{first_name}](tg://user?id={user_id})", parse_mode=enums.ParseMode.MARKDOWN)

    except Exception as e:
        await message.reply(f"An error occurred: {str(e)}")

@Bot.on_message(filters.command("lundbanglist") & filters.private)
async def lund_bang_list(client, message):
    if int(message.from_user.id) not in DEV_ID and int(message.from_user.id) not in OWNER_ID:
        await message.reply("You are not authorized to use this command.")
        return

    try:
        # Fetch all banned users from the blacklist_user collection
        banned_users = await blacklist_users.find({}).to_list(length=100)

        if not banned_users:
            await message.reply("No users are lund banged.")
            return

        # Prepare a message showing all banned users
        bang_list_text = "Lund Banged Users:\n\n"
        for user in banned_users:
            user_id = user["user_id"]
            first_name = user.get("first_name", "Unknown")
            bang_list_text += f"- [{first_name}](tg://user?id={user_id})\n"

        await message.reply(bang_list_text, parse_mode=enums.ParseMode.MARKDOWN)

    except Exception as e:
        await message.reply(f"An error occurred: {str(e)}")
