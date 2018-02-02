import telepot
from telepot.loop import MessageLoop
from time import sleep
import sys
from tycot_bot import TycotBot

bot = telepot.Bot(sys.argv[1])

def handle(msg):
    tycot = TycotBot(bot, msg) 
    tycot.events(msg)  # check if new users entered the chat or left
    print(msg)

    user_cmd = {'/info': tycot.usercmd.info,
                '/ajuda': tycot.usercmd.help,
                '/regras': tycot.usercmd.rules}

    adm_cmd = {'/defwelcome': tycot.admcmd.defwelcome,
               '/defregras': tycot.admcmd.defrules,
               '/ban': tycot.admcmd.ban,
               '/deflink': tycot.admcmd.deflink}

    if tycot.is_adm():
        if msg['text'] in user_cmd:
            user_cmd[msg['text']]()
        else:
            text_cmd = msg['text'].split(' ')[0]
            adm_cmd[text_cmd](msg if msg['text'] == '/ban' else msg['text'])  # gambiarra??
    else:
        user_cmd[msg['text']]()


    # if msg['text'] == '/info':
        # tycot.usercmd.info()
    # elif msg['text'] == '/link':
        # bot.sendMessage(msg['from']['id'], bot.exportChatInviteLink(msg['chat']['id']))
    # elif msg['text'] == '/ajuda':
        # tycot.usercmd.help()
    # elif msg['text'].startswith('/defwelcome'):
        # tycot.admcmd.defwelcome(msg['text'])
    # elif msg['text'] == '/start':
        # tycot.admcmd.start()
    # elif msg['text'].startswith('/defregras'):
        # print(msg['text'])
        # tycot.admcmd.defrules(msg['text'])
    # elif msg['text'] == '/regras':
        # print(msg['text'])
        # tycot.usercmd.rules()
    # elif msg['text'] == '/listadms':
        # bot.sendMessage(tycot.metadata['chat_id'], tycot.admins_ids)


if __name__ == '__main__':
    MessageLoop(bot, handle).run_as_thread()
while True:
    sleep(100)
