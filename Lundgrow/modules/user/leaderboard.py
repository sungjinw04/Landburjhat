import asyncio
from pyrogram import filters, enums
from Lundgrow import Bot
from Lundgrow.database import user_collection

@Bot.on_message(filters.command("chatsins"))
async def chat_sins_leaderboard(client, message):
    chat_id = message.chat.id

    fetching_message = await message.reply("Fetching top lund of this chat...")
    await asyncio.sleep(2)
    await fetching_message.delete()

    top_users = await user_collection.aggregate([
        {"$match": {"chat_id": chat_id}},
        {"$sort": {"dick_size": -1}},
        {"$limit": 10}
    ]).to_list(length=10)

    if not top_users:
        await message.reply("No users have grown their dicks in this chat yet.")
        return

    leaderboard_text = "Top 10 dick sizes in this chat:\n\n"
    for index, user in enumerate(top_users, start=1):
        user_id = user["user_id"]
        first_name = user.get("details", {}).get("first_name", "Unknown")  # Handle missing first_name

        # Format the user as a clickable link
        leaderboard_text += f"{index}) [{first_name}](tg://user?id={user_id}) - {user['dick_size']} cm\n"

    await message.reply(leaderboard_text, parse_mode=enums.ParseMode.MARKDOWN)

@Bot.on_message(filters.command("globalsins"))
async def global_sins_leaderboard(client, message):
    fetching_message = await message.reply("Fetching top lund globally...")
    await asyncio.sleep(2)
    await fetching_message.delete()

    top_users = await user_collection.aggregate([
        {"$group": {
            "_id": "$user_id",
            "total_dick_size": {"$sum": "$dick_size"},
            "first_name": {"$first": "$details.first_name"}
        }},
        {"$sort": {"total_dick_size": -1}},
        {"$limit": 10}
    ]).to_list(length=10)

    if not top_users:
        await message.reply("No users have grown their dicks globally yet.")
        return

    leaderboard_text = "Top 10 global dick sizes:\n\n"
    for index, user in enumerate(top_users, start=1):
        user_id = user["_id"]
        first_name = user.get("first_name", "Unknown")  # Handle missing first_name

        # Format the user as a clickable link
        leaderboard_text += f"{index}) [{first_name}](tg://user?id={user_id}) - {user['total_dick_size']} cm\n"

    await message.reply(leaderboard_text, parse_mode=enums.ParseMode.MARKDOWN)
