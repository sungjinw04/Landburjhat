import random
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto, InputMediaVideo
from Lundgrow import Bot as app
from Lundgrow.database import group_collection
from Lundgrow import BOTLOGS

async def send_message(chat_id: int, message: str):
    await app.send_message(chat_id=chat_id, text=message)

@app.on_message(filters.new_chat_members)
async def on_new_chat_members(client: Client, message: Message):
    total_members = await client.get_chat_members_count(message.chat.id)
    if total_members < 10 and message.chat.id != -1002190382416:
        leave_note = (
            "<b>🚫 Group Limit Reached 🚫</b>\n\n"
            "<i>Sorry! This group has less than 10 members, so I will have to leave... </i>"
        )
        await send_message(message.chat.id, leave_note)
        await client.leave_chat(message.chat.id)
    else:
        for user in message.new_chat_members:
            if user.id == (await client.get_me()).id:
                added_by = message.from_user
                chat_title = message.chat.title
                chat_id = message.chat.id
                chat_username = f"@{message.chat.username}" if message.chat.username else "No Username"
                total_members = await client.get_chat_members_count(chat_id)

                group_info = {
                    "chat_id": chat_id,
                    "chat_title": chat_title,
                    "chat_username": chat_username,
                    "total_members": total_members,
                }
                await group_collection.update_one(
                    {"chat_id": chat_id},
                    {"$set": group_info},
                    upsert=True
                )

                join_text = (
                    "<b>🆕 Bot Added to a New Group 🆕</b>\n\n"
                    f"<b>📍 Group Name:</b> {chat_title}\n"
                    f"<b>🆔 Group ID:</b> {chat_id}\n"
                    f"<b>👥 Total Members:</b> {total_members}\n"
                    f"<b>🔗 Group Link:</b> {chat_username}\n"
                    f"<b>➕ Added By:</b> {added_by.mention}"
                )
                await send_message(BOTLOGS, join_text)

                thanks_message = (
                    f"<b>🙏 Arigato [{added_by.mention}](tg://user?id={added_by.id})</b>\n\n"
                    f"<i>Thank you for adding me to <b>{chat_title}</b>! 🫧💫</i>\n\n"
                    "<i>I'm ready to help your group grow stronger! 💪</i>"
                )
                await send_message(added_by.id, thanks_message)

@app.on_message(filters.left_chat_member)
async def on_left_chat_member(_, message: Message):
    if (await app.get_me()).id == message.left_chat_member.id:
        removed_by = message.from_user.mention if message.from_user else "No User"
        chat_title = message.chat.title
        chat_id = message.chat.id
        chat_username = f"@{message.chat.username}" if message.chat.username else "No Username"
        total_members = await app.get_chat_members_count(chat_id)

        await group_collection.delete_one({"chat_id": chat_id})

        leave_text = (
            "<b>🔴 Bot Left the Group 🔴</b>\n\n"
            f"<b>📍 Group Name:</b> {chat_title}\n"
            f"<b>🆔 Group ID:</b> {chat_id}\n"
            f"<b>👥 Total Members:</b> {total_members}\n"
            f"<b>🔗 Group Link:</b> {chat_username}\n"
            f"<b>❌ Removed By:</b> {removed_by}"
        )
        await app.send_message(BOTLOGS, leave_text)
