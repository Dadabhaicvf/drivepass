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
            sendMarkup(f"<b>𝗛𝗲𝘆{uname},𝗬𝗼𝘂 𝗛𝗮𝘃𝗲𝗻'𝘁 𝗦𝘁𝗮𝗿𝘁𝗲𝗱 𝗠𝗲.! </b>\n\n𝗙𝗿𝗼𝗺 𝗡𝗼𝘄 𝗢𝗻 𝗜 𝗪𝗲𝗹𝗹 𝗚𝗶𝘃𝗲 𝗟𝗶𝗻𝗸 𝗜𝗻 𝗬𝗼𝘂𝗿 𝗣𝗠 𝗢𝗻𝗹𝘆! 😊", bot, update, reply_markup=InlineKeyboardMarkup(keyboard))
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
