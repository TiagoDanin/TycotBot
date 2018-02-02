import telepot
from telepot.loop import MessageLoop
from time import sleep
import sys
from tycot_bot import TycotBot

bot = telepot.Bot(sys.argv[1])

def handle(msg):
    tycot = TycotBot(bot, msg) 
    print(msg)
    tycot.events(msg)

    if msg['text'] == '/info':
        tycot.usercmd.info()
    elif msg['text'] == '/link':
        bot.sendMessage(msg['from']['id'], bot.exportChatInviteLink(msg['chat']['id']))
    elif msg['text'] == '/ajuda':
        tycot.usercmd.help()
    elif msg['text'].startswith('/defwelcome'):
        tycot.admcmd.defwelcome(msg['text'])
    elif msg['text'] == '/start':
        tycot.admcmd.start()
    elif msg['text'].startswith('/defregras'):
        print(msg['text'])
        tycot.admcmd.defrules(msg['text'])
    elif msg['text'] == '/regras':
        print(msg['text'])
        tycot.usercmd.rules()


if __name__ == '__main__':
    MessageLoop(bot, handle).run_as_thread()
while True:
    sleep(100)
