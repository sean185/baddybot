import telegram
import requests as re
from pprint import pprint
from bs4 import BeautifulSoup
from flask import Flask, request
from datetime import date, timedelta
from baddybot.credentials import bot_token, bot_user_name, URL
from baddybot.mastermind import get_response

app = Flask(__name__)

global TOKEN
TOKEN = bot_token
global bot
bot = telegram.Bot(token=TOKEN)

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
            if len(content) == 2:
                CC = content[0]
                bdate = datetime.strptime(content[1], '%Y-%m-%d').date()
                response = getAvailability(CC, bdate)
            else:
                response = getAvailability('4330ccmcpa-bm', date.today()+timedelta(days=16))
        else:
            response = "You sent for the command: {}\nParameters in context: {}".format(command, content)
        bot.sendMessage(chat_id=chat_id, text=response)
    else:
        # do nothing unless it's a command
        pass

    return 'ok'

@app.route('/setwebhook', methods=['GET', 'POST'])
def set_webhook():
    # we use the bot object to link the bot to our app which live
    # in the link provided by URL
    s = bot.setWebhook('{URL}/{HOOK}'.format(URL=URL, HOOK=TOKEN))

    # something to let us know things work
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"

@app.route('/')
def hello():
    return "Hello World!"

if __name__ == '__main__':
    app.run(threaded=True)
