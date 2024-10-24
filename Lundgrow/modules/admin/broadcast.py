import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from Lundgrow import Bot as app
from Lundgrow.database import user_collection, group_collection
from ...config import DEV_ID, OWNER_ID

broadcast_cancelled = False


async def send_message_to_groups(client: Client, message: Message):
    global broadcast_cancelled
    broadcast_cancelled = False
    total_groups = 0
    total_users = 0

    broadcast_message = await message.reply_text(
        "Broadcasting.....",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Cancel Broadcast ❌❌", callback_data="cancel_broadcast")]
        ])
    )

    # Broadcast to groups
    async for group in group_collection.find():
        if broadcast_cancelled:
            await broadcast_message.edit_text("Broadcast cancelled.")
            return
        try:
            await client.send_message(group['chat_id'], message.reply_to_message.text)
            total_groups += 1
        except Exception as e:
            print(f"Failed to send to group {group['chat_id']}: {e}")

    # Broadcast to user PMs
    async for user in user_collection.find():
        if broadcast_cancelled:
            await broadcast_message.edit_text("Broadcast cancelled.")
            return
        try:
            await client.send_message(user['id'], message.reply_to_message.text)
            total_users += 1
        except Exception as e:
            print(f"Failed to send to user {user['id']}: {e}")

    await broadcast_message.edit_text(f"Broadcast successfully sent to {total_users} users and {total_groups} groups.")
    for dev_id in DEV_ID + OWNER_ID:
        await client.send_message(dev_id, f"Broadcast completed. Sent to {total_users} users and {total_groups} groups.")


@app.on_message(filters.command("bcast") & filters.reply)
async def broadcast(client: Client, message: Message):
    if int(message.from_user.id) not in DEV_ID and int(message.from_user.id) not in OWNER_ID:
        return

    await send_message_to_groups(client, message)


@app.on_message(filters.command("ucast") & filters.reply)
async def user_broadcast(client: Client, message: Message):
    if int(message.from_user.id) not in DEV_ID and int(message.from_user.id) not in OWNER_ID:
        return

    broadcast_cancelled = False
    total_users = 0

    broadcast_message = await message.reply_text(
        "Broadcasting to users.....",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Cancel Broadcast ❌❌", callback_data="cancel_broadcast")]
        ])
    )

    # Broadcast to user PMs
    async for user in user_collection.find():
        if broadcast_cancelled:
            await broadcast_message.edit_text("Broadcast cancelled.")
            return
        try:
            await client.send_message(user['id'], message.reply_to_message.text)
            total_users += 1
        except Exception as e:
            print(f"Failed to send to user {user['id']}: {e}")

    await broadcast_message.edit_text(f"Broadcast successfully sent to {total_users} users.")
    for dev_id in DEV_ID + OWNER_ID:
        await client.send_message(dev_id, f"User broadcast completed. Sent to {total_users} users.")


@app.on_callback_query(filters.regex("cancel_broadcast"))
async def cancel_broadcast(client: Client, callback_query: CallbackQuery):
    global broadcast_cancelled
    broadcast_cancelled = True
    await callback_query.message.edit_text("Broadcasting cancelled.")
    await callback_query.answer("Broadcast cancelled successfully.", show_alert=True)
