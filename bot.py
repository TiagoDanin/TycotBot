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
                '/regras': tycot.usercmd.rules,
                '/link': tycot.usercmd.link}

    adm_cmd = {'/defwelcome': tycot.admcmd.defwelcome,
               '/defmaxwarn': tycot.admcmd.maxwarn,
               '/warn': tycot.admcmd.warn,
               '/unwarn': tycot.admcmd.unwarn,
               '/defregras': tycot.admcmd.defrules,
               '/ban': tycot.admcmd.ban,
               '/deflink': tycot.admcmd.deflink,
               '/start': tycot.admcmd.start}

# TODO: melhorar issu
    text_cmd = msg['text'].split(' ')[0]
    if text_cmd in user_cmd:
        user_cmd[text_cmd]()
    elif text_cmd in adm_cmd:
        if tycot.is_adm():
            if text_cmd == '/start' or text_cmd == '/warn' or text_cmd == '/unwarn':
                adm_cmd[text_cmd]()
            else:
                # solução temporaria
                if text_cmd == '/ban':
                    adm_cmd[text_cmd](msg)
                else:
                    adm_cmd[text_cmd](msg['text'])
        else:
            user_cmd[msg['text']]()


if __name__ == '__main__':
    MessageLoop(bot, handle).run_as_thread()
while True:
    sleep(50)
