from telegram.message import Message
from telegram.update import Update
import time
from bot import LOGGER, bot
from telegram.error import TimedOut, BadRequest
from bot import bot
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.message import Message
from telegram.update import Update


def sendMarkup(text: str, bot, update: Update, reply_markup: InlineKeyboardMarkup):
    try:
        return bot.send_message(update.message.chat_id,
                            reply_to_message_id=update.message.message_id,
                            text=text, reply_markup=reply_markup, allow_sending_without_reply=True,
                            parse_mode='HTMl', disable_web_page_preview=True)
    except RetryAfter as r:
        LOGGER.error(str(r))
        time.sleep(r.retry_after * 1.5)
        return sendMarkup(text, bot, update, reply_markup)
    except Exception as e:
        LOGGER.error(str(e))
        

def sendMessage(text: str, bot, update: Update):
    try:
        return bot.send_message(update.message.chat_id,
                            reply_to_message_id=update.message.message_id,
                            text=text, parse_mode='HTMl')
    except Exception as e:
        LOGGER.error(str(e))
        
def sendPrivate(text: str, bot, update: Update, reply_markup: InlineKeyboardMarkup):
    bot_d = bot.get_me()
    b_uname = bot_d.username
    
    try:
        return bot.send_message(update.message.from_user.id,
                             reply_to_message_id=update.message.message_id,
                             text=text, disable_web_page_preview=True, reply_markup=reply_markup, allow_sending_without_reply=True, parse_mode='HTMl')
    except Exception as e:
        LOGGER.error(str(e))
        if "Forbidden" in str(e):
            uname = f'<a href="tg://user?id={update.message.from_user.id}">{update.message.from_user.first_name}</a>'
            keyboard = [
            [InlineKeyboardButton("Start Me", url = "http://t.me/DadaDrive_Bot?start=start")],
            [InlineKeyboardButton("Join Here", url = "https://t.me/DadaXClouds")]]
            sendMarkup(f"<b>ʜᴇʏ {uname}, ʏᴏᴜ ʜᴀᴠᴇɴ'ᴛ sᴛᴀʀᴛᴇᴅ ᴍᴇ ɪɴ ᴘᴍ (ᴘʀɪᴠᴀᴛᴇ ᴄʜᴀᴛ) ʏᴇᴛ👀.</b>\n\n𝐅𝐑𝐎𝐌 𝐍𝐎𝐖 𝐎𝐍 𝐈 𝐖𝐈𝐋𝐋 𝐆𝐈𝐕𝐄 𝐋𝐈𝐍𝐊 𝐈𝐍 𝐏𝐌 (𝐏𝐑𝐈𝐕𝐀𝐓𝐄 𝐂𝐇𝐀𝐓) 𝐎𝐍𝐋𝐘 😁", bot, update, reply_markup=InlineKeyboardMarkup(keyboard))
            return        

def editMessage(text: str, message: Message, reply_markup=None):
    try:
        bot.edit_message_text(text=text, message_id=message.message_id,
                              chat_id=message.chat.id,reply_markup=reply_markup,
                              parse_mode='HTMl')
    except Exception as e:
        LOGGER.error(str(e))
        
def deleteMessage(bot, message: Message):
    try:
        bot.delete_message(chat_id=message.chat.id,
                           message_id=message.message_id)
    except Exception as e:
        LOGGER.error(str(e))

def sendLogFile(bot, update: Update):
    with open('log.txt', 'rb') as f:
        bot.send_document(document=f, filename=f.name,
                          reply_to_message_id=update.message.message_id,
                          chat_id=update.message.chat_id)
