from pyrogram import filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from Lundgrow import Bot
from Lundgrow.database import blacklist_collection
from ...config import OWNER_ID, DEV_ID

@Bot.on_message(filters.command("blchat") & filters.private)
async def blacklist_chat(client, message):
    if int(message.from_user.id) not in DEV_ID and int(message.from_user.id) not in OWNER_ID:
        await message.reply("You are not authorized to use this command.")
        return

    try:
        # Get the chat_id to blacklist from the command argument
        chat_id = int(message.command[1])
        
        # Fetch chat information to get the chat's title or username
        chat = await client.get_chat(chat_id)
        chat_title = chat.title or chat.username or str(chat_id)

        # Check if the chat is already blacklisted
        existing = await blacklist_collection.find_one({"chat_id": chat_id})
        if existing:
            await message.reply("This chat is already blacklisted.")
            return

        # Insert the chat_id into the blacklist_collection
        await blacklist_collection.insert_one({"chat_id": chat_id})

        # Send a success message
        chat_info = f'[{chat_title}](tg://user?id={chat_id})' if chat_title != str(chat_id) else f"`{chat_id}`"
        await message.reply(f"Successfully added {chat_info} to the blacklist.", parse_mode=enums.ParseMode.MARKDOWN)

    except IndexError:
        await message.reply("Please provide a valid chat ID.")
    except Exception as e:
        await message.reply(f"An error occurred: {str(e)}")

@Bot.on_message(filters.command("blchatlist") & filters.private)
async def blacklist_chat_list(client, message):
    if int(message.from_user.id) not in DEV_ID and int(message.from_user.id) not in OWNER_ID:
        await message.reply("You are not authorized to use this command.")
        return

    try:
        # Fetch all blacklisted chats from the database
        blacklisted_chats = await blacklist_collection.find({}).to_list(length=100)
        
        if not blacklisted_chats:
            await message.reply("No chats are blacklisted.")
            return

        # Prepare a message showing all blacklisted chats
        blacklist_text = "Blacklisted Chats:\n\n"
        for chat in blacklisted_chats:
            chat_id = chat["chat_id"]
            try:
                # Try fetching chat info for each blacklisted chat
                chat_info = await client.get_chat(chat_id)
                chat_title = chat_info.title or chat_info.username or str(chat_id)
            except:
                # In case the chat no longer exists or can't be accessed
                chat_title = f"`{chat_id}`"

            blacklist_text += f"- {chat_title}\n"

        await message.reply(blacklist_text, parse_mode=enums.ParseMode.MARKDOWN)

    except Exception as e:
        await message.reply(f"An error occurred: {str(e)}")
