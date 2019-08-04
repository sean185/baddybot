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

@app.route('/{}'.format(TOKEN), methods=['POST'])
def respond():
    # retrieve the message in JSON and then transform it to Telegram object
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    pprint("got update:", update)

    chat_id = update.message.chat.id # chatroom ID
    msg_id = update.message.message_id # reference that allows you to reply to a message

    # Telegram understands UTF-8, so encode text for unicode compatibility
    text = update.message.text.encode('utf-8').decode()

    if text.startswith('/'):
        command = text.split()[0]
        content = text[len(command)+1:]
        if command == '/getcourts':
            response = getAvailability('4330ccmcpa-bm', date.today()+timedelta(days=16))
        else:
            response = "You sent for the command: {}\nParameters in context: {}".format(command, content)
        bot.sendMessage(chat_id=chat_id, text=response)
    else:
        # do nothing unless it's a command
        pass

    return 'ok'



STATUSMAP = {
    'normal':'N',
    'peak':'P',
    'booked':'B',
    'notAvailable':'NA'
}

def getAvailability(CCcode, bookingdate):
    res = re.get('https://www.onepa.sg/facilities/{}?date={}'.format(CCcode, bookingdate))
    soup = BeautifulSoup(res.text, 'html.parser')

    times = [x for x in soup.find(id='facTable1').select('.timeslotsContainer .slots')]
    times = [x.text.split(' - ')[0].strip(' ') for x in times]

    courts = soup.find(id='facTable1').select('.facilitiesType')

    availability = []
    for court in courts:
        slots = court.select('.slots')
        slots = [list(slot.attrs['class'])[-1] for slot in slots]
        slots = [STATUSMAP[s] for s in slots]
        availability.append(slots)

    rows = list(zip(*[times]+availability))

    output = []
    for r in rows:
        output.append('|'.join([r[0].rjust(8)]+[i.ljust(3) for i in r[1:]]))

    return '\n'.join(output)

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
