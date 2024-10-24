from pyrogram import filters, enums
from Lundgrow import OWNER_ID, DEV_ID, Bot
from Lundgrow.database import special_user_collection

@Bot.on_message(filters.command("add") & filters.user([OWNER_ID, DEV_ID]) & filters.reply)
async def add_special_user(client, message):
    # Get the replied-to user's ID
    target_user_id = message.reply_to_message.from_user.id
    target_first_name = message.reply_to_message.from_user.first_name

    
    if special_user_collection.find_one({"user_id": target_user_id}):
        await message.reply(f"{target_first_name} is already in the special dick grower list.")
        return

    
    special_user_collection.insert_one({"user_id": target_user_id})

    
    await message.reply(f"Successfully added [{target_first_name}](tg://user?id={target_user_id}) to the special dick grower list.", parse_mode=enums.ParseMode.MARKDOWN)
