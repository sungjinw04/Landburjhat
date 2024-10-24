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

    
    existing_user = await special_user_collection.find_one({"user_id": target_user_id})
    
    if existing_user:
        await message.reply(f"{target_first_name} is already in the special list.")
        return

    await special_user_collection.insert_one({"user_id": target_user_id, "first_name": target_first_name})

    await message.reply(f"Successfully added [{target_first_name}](tg://user?id={target_user_id}) to the special list.", parse_mode=enums.ParseMode.MARKDOWN)


@Bot.on_message(filters.command("remove") & filters.reply)
async def remove_special_user(client, message):
    if int(message.from_user.id) not in DEV_ID and int(message.from_user.id) not in OWNER_ID:
        return

    target_user_id = message.reply_to_message.from_user.id
    target_first_name = message.reply_to_message.from_user.first_name

    existing_user = await special_user_collection.find_one({"user_id": target_user_id})
    
    if not existing_user:
        await message.reply(f"{target_first_name} is not in the special list.")
        return

    await special_user_collection.delete_one({"user_id": target_user_id})

    await message.reply(f"Successfully removed [{target_first_name}](tg://user?id={target_user_id}) from the special list.", parse_mode=enums.ParseMode.MARKDOWN)


@Bot.on_message(filters.command("lundlog"))
async def list_special_users(client, message):
    if int(message.from_user.id) not in DEV_ID and int(message.from_user.id) not in OWNER_ID:
        return

    special_users = special_user_collection.find()

    user_links = []
    async for user in special_users:
        first_name = user.get("first_name", "Unknown")
        user_id = user["user_id"]
        user_link = f"[{first_name}](tg://user?id={user_id})"
        user_links.append(user_link)

    if not user_links:
        await message.reply("The special list is currently empty.")
    else:
        user_links_text = "\n".join(user_links)
        await message.reply(user_links_text, parse_mode=enums.ParseMode.MARKDOWN)
