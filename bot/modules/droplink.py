import re
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

from telegram.ext import CommandHandler
from bot.helper.ext_utils.exceptions import DDLException
from bot.helper.drive_utils.gdriveTools import GoogleDriveHelper
from bot import LOGGER, dispatcher
from bot.helper.telegram_helper.message_utils import *
from bot.helper.telegram_helper.filters import CustomFilters
from bot.helper.telegram_helper.bot_commands import 


# droplink url
def link_handler(update, context):
    args = update.message.text.split(" ", maxsplit=1)
    if len(args) > 1:
        link = args[1]
    else:
        link = ''
    try:
      is_droplink = True if "droplink" in link else False
      if is_droplink:
          msg = sendMessage(f'𝗕𝘆𝗽𝗮𝘀𝘀𝗶𝗻𝗴 𝘆𝗼𝘂𝗿 𝗗𝗿𝗼𝗽𝗹𝗶𝗻𝗸 𝗟𝗶𝗻𝗸: <code>{link}</code>\n\n𝙋𝙡𝙚𝙖𝙨𝙚 𝙬𝙖𝙞𝙩 𝙖 𝙢𝙞𝙣𝙪𝙩𝙚.', context.bot, update)
          baashax = droplink_bypass(link)
          links = baashax.get('url')
          deleteMessage(context.bot, msg)
          sendMessage(f"𝗚𝗶𝘃𝗲𝗻 𝗟𝗶𝗻𝗸: <code>{link}</code>\n\n𝗕𝘆𝗽𝗮𝘀𝘀𝗲𝗱 𝗟𝗶𝗻𝗸: <code>{links}</code>", context.bot, update)
      else:
          sendMessage('𝗦𝗲𝗻𝗱 𝗗𝗿𝗼𝗽𝗹𝗶𝗻𝗸 𝗟𝗶𝗻𝗸𝘀 𝗮𝗹𝗼𝗻𝗴 𝘄𝗶𝘁𝗵 𝗰𝗼𝗺𝗺𝗮𝗻𝗱.', context.bot, update)
    except DDLException as e:
        LOGGER.error(e)

# ==============================================
    
def droplink_bypass(url):
    client = requests.Session()
    res = client.get(url)

    ref = re.findall("action[ ]{0,}=[ ]{0,}['|\"](.*?)['|\"]", res.text)[0]

    h = {'referer': ref}
    res = client.get(url, headers=h)

    bs4 = BeautifulSoup(res.content, 'lxml')
    inputs = bs4.find_all('input')
    data = { input.get('name'): input.get('value') for input in inputs }

    h = {
        'content-type': 'application/x-www-form-urlencoded',                        
        'x-requested-with': 'XMLHttpRequest'
    }
    p = urlparse(url)
    final_url = f'{p.scheme}://{p.netloc}/links/go'

    time.sleep(3.1)
    res = client.post(final_url, data=data, headers=h).json()

    return res


droplink_handler = CommandHandler(BotCommands.DropCommand, link_handler,
                               filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True)
dispatcher.add_handler(droplink_handler)
