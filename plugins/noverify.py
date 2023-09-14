from info import *
from utils import *
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery 
import asyncio

bot_uname = "Pm_link_yojana_bot"

# Define a dictionary to store user states
user_states = {}
@Client.on_message(filters.group & filters.command("reset_grp"))
async def _reset_grp(bot, message):
    try:
        group = await get_group(message.chat.id)
        user_id = group["user_id"]
        user_name = group["user_name"]
        verified = group["verified"]
    except:
        add_button = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("ᴀᴅᴅ ᴍᴇ ʙᴀᴄᴋ 👻", url=f"http://telegram.me/{bot_uname}?startgroup=true")]
            ]
        )
        await message.reply("<b>I ʟᴇғᴛ ᴛʜɪs ᴄʜᴀᴛ,\n\nᴘʟᴇᴀsᴇ ᴀᴅᴅ ᴍᴇ ᴀɢᴀɪɴ ʙʏ ᴄʟɪᴄᴋɪɴɢ ᴛʜᴇ ʙᴜᴛᴛᴏɴ ʙᴇʟᴏᴡ 👇🏻</b>", reply_markup=add_button)
        return await bot.leave_chat(message.chat.id)

    try:
        user = await bot.get_users(user_id)
    except:
        return await message.reply(f"❌ {user_name} Need to start me in PM!")

    if message.from_user.id != user_id:
        return await message.reply(f"<b>Oɴʟʏ {user.mention} ᴄᴀɴ ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ 😁</b>")

    if verified == True:
        # Ask the user if they want to continue the process
        continue_button = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("Yes", callback_data="continue"), InlineKeyboardButton("No", callback_data="cancel")]
            ]
        )

        await message.reply("<b>Dᴏ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴄᴏɴᴛɪɴᴜᴇ ᴛʜɪs ᴘʀᴏᴄᴇss?\n\nNᴏᴛᴇ:Iғ ʙᴏᴛ ɪs ʀᴜɴɴɪɴɢ ɪɴ ᴛʜɪs ɢʀᴏᴜᴘ ᴘʀᴏᴘᴇʀʟʏ ᴊᴜsᴛ ᴄʟɪᴄᴋ 'NO' ᴛᴏ ᴄᴀɴᴄᴇʟ(Hɪɢʜ Wᴀʀɴɪɴɢ).\n\nɪғ ʙᴏᴛ ɪs ᴄᴏɴɴᴇᴄᴛᴇᴅ ᴡɪᴛʜ ʏᴏᴜʀ ᴄʜᴀɴɴᴇʟs(ᴡɪᴛʜ ᴀᴅᴍɪɴ ʀɪɢʜᴛs) ʙᴜᴛ ɴᴏᴛ ɢɪᴠɪɴɢ ʟɪɴᴋs ɪɴ ᴛʜɪs ɢʀᴏᴜᴘ,ᴄʟɪᴄᴋ 'ʏᴇs' ᴛᴏ ᴄᴏɴᴛɪɴᴜᴇ.\nᴄʜᴇᴄᴋ ᴛʜᴇ ᴄᴏɴɴᴇᴄᴛɪᴏɴ ʟɪsᴛ ʙʏ /connections ᴄᴏᴍᴍᴀɴᴅ</b>", reply_markup=continue_button)
        
        # Set the user's state to "waiting_for_confirmation"
        user_states[message.chat.id] = "waiting_for_confirmation"
        
        return

    try:
        link = (await bot.get_chat(message.chat.id)).invite_link
    except:
        return message.reply("❌ Make me admin here with all permissions!")
@Client.on_callback_query(filters.regex("^(continue|cancel)$"))
async def callback_handler(bot, query: CallbackQuery):
    chat_id = query.message.chat.id  # Moved this line here to get the chat_id

    if chat_id in user_states and user_states[chat_id] == "waiting_for_confirmation":
        if query.data == "continue":
            group = await get_group(chat_id)  # Changed message.chat.id to chat_id
            user_id = group["user_id"]
            user_name = group["user_name"]
            # Handle the "Yes" button click
            await query.answer("You clicked Yes. Continue with the process.")

            await delete_group(chat_id)  # Changed message.chat.id to chat_id
            add_button = InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("ᴀᴅᴅ ᴍᴇ ʙᴀᴄᴋ 👻", url=f"http://telegram.me/{bot_uname}?startgroup=true")]
                ]
            )
            await query.message.edit_text("<b>Tʜᴇ ɢʀᴏᴜᴘ ʜᴀs ʙᴇᴇɴ sᴜᴄᴄᴇssғᴜʟʟʏ ᴜɴᴠᴇʀɪғɪᴇᴅ🥶.\n\n Tᴏ ʀᴇɢᴀɪɴ ᴠᴇʀɪғɪᴄᴀᴛɪᴏɴ ᴀᴄᴄᴇss,ᴘʟᴇᴀsᴇ ᴀᴅᴅ ᴍᴇ ᴀɢᴀɪɴ ʙʏ ᴄʟɪᴄᴋɪɴɢ ᴛʜᴇ ʙᴜᴛᴛᴏɴ ʙᴇʟᴏᴡ 👇🏻</b>", reply_markup=add_button)
            return await bot.leave_chat(chat_id)  # Changed message.chat.id to chat_id
        elif query.data == "cancel":
            # Handle the "No" button click
            await query.answer("Yᴏᴜ ᴄʟɪᴄᴋᴇᴅ Nᴏ. Pʀᴏᴄᴇss ᴄᴀɴᴄᴇʟᴇᴅ.")
            # Edit the message to indicate the process is canceled
            await query.message.edit_text("<b>Pʀᴏᴄᴇss ᴄᴀɴᴄᴇʟᴇᴅ.</b>")
            await asyncio.sleep(4)
            await query.message.delete()  # Delete bot's message
            await query.message.reply_to_message.delete()  # Delete user's message
            return
        # Remove the user's state
        del user_states[chat_id]


if __name__ == "__main__":
    app.run()
