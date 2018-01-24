import telepot
from telepot.loop import MessageLoop
from time import sleep
import sys
from tycot_bot import TycotBot

bot = telepot.Bot(sys.argv[1])

def handle(msg):
    tycot = TycotBot(bot, msg) 
    print(msg)
    print(bot.getChatAdministrators(msg['chat']['id']))
    if msg['text'] == '/info':
        tycot.usercmd.info()
    elif msg['text'] == '/link':
        print(bot.exportChatInviteLink(msg['chat']['id']))
    elif msg['text'] == '/ajuda':
        tycot.usercmd.help()
    elif msg['text'] == '/defwelcome':
        tycot.admcmd.defwelcome(msg['text'])


if __name__ == '__main__':
    MessageLoop(bot, handle).run_as_thread()
while True:
    sleep(100)
