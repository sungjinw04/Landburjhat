from pyrogram import filters, enums
from ...config import OWNER_ID, DEV_ID
from Lundgrow import Bot
from Lundgrow.database import special_user_collection

@Bot.on_message(filters.command("add") & filters.reply)
async def add_special_user(client, message):
    if int(message.from_user.id) not in DEV_ID and int(message.from_user.id) not in OWNER_ID:
        return

    target_user_id = message.reply_to_message.from_user.id
    target_first_name = message.reply_to_message.from_user.first_name

    if special_user_collection.find_one({"user_id": target_user_id}):
        await message.reply(f"{target_first_name} is already in the special list.")
        return

    special_user_collection.insert_one({"user_id": target_user_id})

    await message.reply(f"Successfully added [{target_first_name}](tg://user?id={target_user_id}) to the special list.", parse_mode=enums.ParseMode.MARKDOWN)


@Bot.on_message(filters.command("remove") & filters.reply)
async def remove_special_user(client, message):
    if int(message.from_user.id) not in DEV_ID and int(message.from_user.id) not in OWNER_ID:
        return

    target_user_id = message.reply_to_message.from_user.id
    target_first_name = message.reply_to_message.from_user.first_name

    if not special_user_collection.find_one({"user_id": target_user_id}):
        await message.reply(f"{target_first_name} is not in the special list.")
        return

    special_user_collection.delete_one({"user_id": target_user_id})

    await message.reply(f"Successfully removed [{target_first_name}](tg://user?id={target_user_id}) from the special list.", parse_mode=enums.ParseMode.MARKDOWN)
