import telepot
import time
from datetime import datetime
from telepot.loop import MessageLoop
from pprint import pprint

now = datetime.now()
bot = telepot.Bot(str(input('TOKEN> ')))
updates = bot.getUpdates()
print(updates)

print("Bot inicializado!")

def welcome(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    try:
        new_member = msg['new_chat_member']['first_name']
    except:
        new_member = 'Novo Membro'
    if(content_type == 'new_chat_member'):
        get_bot_name = bot.getMe()
        bot_name = get_bot_name['first_name']
        #bot_username = '@{}'.format(get_bot_name['username'])
        if(new_member == bot_name):
            bot.sendMessage(chat_id, 'Olá, sou o PygrameirosBot!')
        else:
            bot.sendMessage(chat_id,'Seja bem vindo ao Pygrameiros, '+new_member+'!')

def rules(msg):
    text = str(msg['text'])
    if(text[0:9] == "/setrules"):
        user_id = msg['from']['id']
        admins = bot.getChatAdministrators(msg['chat']['id'])
        adm_list = [adm['user']['id'] for adm in admins]
        if (user_id in adm_list):
            text = text.replace("/setrules ", "")
            rules = open('rules.txt', 'w')
            rules.write(text)
            rules.close()
            bot.sendMessage(msg['chat']['id'], "As novas regras foram salvas com sucesso!")

    if(text[0:7] == "/rules"):
            rules = open('rules.txt', 'r')
            rules = rules.read()
            bot.sendMessage(msg['chat']['id'], rules)

def commands(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if(chat_type == 'private'):
        if(msg['chat']['id'] == '/start' or msg['chat']['id'] == '/start@PygrameirosBot'):
            bot.sendMessage(chat_id, "Olá, eu sou o Pybot!\nFui criado pela galera do Pygrameiros para te ajudar a administrar teu grupo!")
            log(msg)

    if(msg['chat']['id'] == '/info' or msg['chat']['id'] == '/info@PygrameirosBot'):
        bot.sendMessage(str(chat_id), str("ID INFO \n\n NOME: " + username + " \n ID: " + str(user_id) + " \n NOME DO GRUPO: " + chat_title + " \n ID GROUP: " + str(chat_id)) ,reply_to_message_id=str(message_id))
        log(msg)


    if(msg['chat']['id'] == '/link' or msg['chat']['id'] == '/link@PygrameirosBot'):
        bot.sendMessage(chat_id, 'Nosso link é: https://goo.gl/m0h2eQ')
        log(msg)

    if(msg['chat']['id'] == '/help' or msg['chat']['id'] == '/help@PygrameirosBot'):
        bot.sendMessage(chat_id, 'Olá, sou o PygrameirosBot!\nSegue a minha lista de comandos:\n/info -> Informações do grupo\n/link -> Link do grupo')
        log(msg)

def log(msg):
    day = str(now.day)
    month = str(now.month)
    year = str(now.year)
    hour = str(now.hour)
    minute = str(now.minute)
    second = str(now.second)

    chat_type = telepot.glance(msg)
    log = open('log.txt', 'a')
    users_register = open('users_register.txt', 'a')

    if(msg['text'] == '/start' or msg['text'] == '/start@PygrameirosBot'):
        users_register.write(str("log [" + day + "/" + month + "/" + year + "][" + hour + ":" + minute + ":" + second + "]"))
        users_register.write(str(" | Username: " + str(msg['from']['username']) + " | ID: " + str(msg['from']['id']) + " | Comando usado: " + str(msg['text']) + "\n"))
        users_register.close()
        print("@"+ str(msg['from']['username']) + " Iniciou o Bot - Dados salvos!")

    else:
        log.write(str("log [" + day + "/" + month + "/" + year + "][" + hour + ":" + minute + ":" + second + "]"))
        log.write(str(" | Username: " + str(msg['from']['username']) + " | ID: " + str(msg['from']['id']) + " | Comando usado: " + str(msg['text']) + " | ChatType: " + str(chat_type) + " | Chat ID: " + str(chat_id) + "\n"))
        log.close()
        print("@"+ str(msg['from']['username']) + " Usou o Bot! - Dados salvos!")

def handle(msg):
    welcome(msg)
    commands(msg)
    rules(msg)
    print(msg['text'])



MessageLoop(bot, handle).run_as_thread()
while 1:
    time.sleep(10)
