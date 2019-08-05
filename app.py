import requests as re
from pprint import pprint
from bs4 import BeautifulSoup
from flask import Flask, request
from datetime import datetime, date, timedelta

import telegram
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from baddybot.credentials import bot_token, bot_user_name, URL
from baddybot.mastermind import get_response
from baddybot import crawlers
from baddybot.constants import WISHLIST, COMMUNITYCLUBS

app = Flask(__name__)

global TOKEN
TOKEN = bot_token
global bot
bot = telegram.Bot(token=TOKEN)
global CCLIST
CCLIST = [COMMUNITYCLUBS[i] for i in WISHLIST]

## Basic requirement to establish the webhook
@app.route('/setwebhook', methods=['GET', 'POST'])
def set_webhook():
    s = bot.setWebhook('{URL}/{HOOK}'.format(URL=URL, HOOK=TOKEN))
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"

def handle_getCourts():
    # if len(content) == 2:
    #     CC = content[0]
    #     bdate = datetime.strptime(content[1], '%Y-%m-%d').date()
    #     response = crawlers.getAvailability(CC, bdate)
    # else:
    #     response = crawlers.getAvailability('4330ccmcpa-bm', date.today()+timedelta(days=16))
    keyboard = [[InlineKeyboardButton(CC[1], callback_data=CC[0])] for CC in CCLIST]
    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup

## Main handler for any messages transmitted via the webhook
@app.route('/{}'.format(TOKEN), methods=['POST'])
def respond():
    # retrieve the message in JSON and then transform it to Telegram object
    app.logger.debug('received update')
    json_res = request.get_json(force=True)
    pprint(json_res)
    update = telegram.Update.de_json(json_res, bot)
    # print("got update:", update)

    # only able to handle direct chat messages for now
    if not hasattr(update.message, 'chat'):
        return 'ok'

    chat_id = update.message.chat.id # chatroom ID
    msg_id = update.message.message_id # reference that allows you to reply to a message
    text = update.message.text.encode('utf-8').decode()

    if text.startswith('/'):
        command = text.split()[0]
        content = text[len(command)+1:].split()
        if command == '/getcourts':
            reply = handle_getCourts()
            bot.sendMessage(chat_id=chat_id, text='Please choose:', reply_markup=reply)
        else:
            reply = "Unsupported command: {}".format(command)
            bot.sendMessage(chat_id=chat_id, text=reply)

    return 'ok'

if __name__ == '__main__':
    app.run(threaded=True)
