import telepot
import time
from datetime import datetime
from telepot.loop import MessageLoop
from pprint import pprint

now = datetime.now()
bot = telepot.Bot('TOKEN')
updates = bot.getUpdates()
print(updates)

print("Bot inicializado!")
def rules(msg):
    if('/setrules' in (msg['text'])):
        get_admins = bot.getChatAdministrators(msg['chat']['id'])
        #admins_list = get_admins(['status'])
        print(get_admins)
        print('=====\n')
        print(msg['chat']['id'])

        """if('ChatMember' == "creator"):
            print(username + " usou o comando /rules em: " + time)
            text = text.replace("/setrules ", "")
            rules = open('rules.txt', 'w')
            rules.write(text)
            rules.close()
            bot.sendMessage(msg['chat']['id'], "As novas regras foram salvas com sucesso!")"""

    if((msg['text']) == "/rules"):
        rules = open('rules.txt', 'r')
        rules = rules.read()
        bot.sendMessage(msg['chat']['id'], rules)

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)

    try:
        chat_title = str(msg['chat']['title'])
    except:
        chat_title = ''
    try:
        text = str(msg['text'])
    except:
        text = ""
    try:
        message_id = float(msg['Message']['message_id']) #Identificador da mensagem
    except:
        message_id = None
    try:
        user_id = float(msg['from']['id'])
    except:
        user_id = 0.0
    try:
        first_name = str(msg['from']['first_name'])
    except:
        first_name = ''
    try:
        last_name = str(msg['from']['last_name'])
    except:
        last_name = ''
    try:
        username = str(msg['from']['username'])
    except:
        username = ""
    try:
        new_member = msg['new_chat_member']['first_name']
    except:
        new_member = 'Novo Membro'
    try:
        chat_member = str(msg['chat_member']['status'])
    except:
        chat_member = "member"

    day = str(now.day)
    month = str(now.month)
    year = str(now.year)
    hour = str(now.hour)
    minute = str(now.minute)
    second = str(now.second)
    time = (hour+':'+minute+':'+second+' -> '+day+'/'+month+'/'+year)

    users = open('users-register.txt', 'a')
    log = open('log_comands.txt', 'a')

    rules(msg)
    #boas-vindas
    #corrigir o bug que ele dá boas vindas a si mesmo
    if( content_type == 'new_chat_member'):
        get_bot_name = bot.getMe()
        bot_name = get_bot_name['first_name']
        #bot_username = '@{}'.format(get_bot_name['username'])
        if(new_member == bot_name):
            bot.sendMessage(chat_id, 'Olá, sou o PygrameirosBot!')
        else:
            bot.sendMessage(chat_id,'Seja bem vindo ao Pygrameiros, '+new_member+'!')

    if(chat_type == 'private'):
        if(text == '/start' or '/start@PygrameirosBot'):
            print(username + " iniciou o bot em: " + time)
            bot.sendMessage(chat_id, "Olá, eu sou o Pybot!\nFui criado pela galera do Pygrameiros para te ajudar a administrar teu grupo!")
            #Salvando os dados no arquivo users
            users.write(str("log [" + day + "/" + month + "/" + year + "][" + hour + ":" + minute + ":" + second + "]"))
            users.write(str(" | Username: " + username + " | ID: " + str(user_id) + " | Comando usado: " + text + " | Chat: " + chat_type + "\n"))
            users.close()
            print("@"+username + " ("+ first_name + " " + last_name + ") " + " Iniciou o Bot - Dados salvos!")
    if(text == '/info' or text == '/info@PygrameirosBot'):
        print(username + " usou o comando /info em: " + time)
        bot.sendMessage(str(chat_id), str("ID INFO \n\n NOME: " + username + " \n ID: " + str(user_id) + " \n NOME DO GRUPO: " + chat_title + " \n ID GROUP: " + str(chat_id)) ,reply_to_message_id=str(message_id))
        log.write(str("log [" + day + "/" + month + "/" + year + "][" + hour + ":" + minute + ":" + second + "]"))
        log.write(str(" | Username: " + username + " | ID: " + str(user_id) + " | Comando usado: " + text + " | ChatType: " + chat_type + " | Chat ID: " + str(chat_id) + "\n"))
        log.close()
        print("@"+username + " ("+ first_name + " " + last_name + ") " + " Usou o Bot! - Dados salvos!")

    if(text == '/link' or text == '/link@PygrameirosBot'):
        print(username + " usou o comando /link em: " + time)
        bot.sendMessage(chat_id, 'Nosso link é: https://goo.gl/m0h2eQ')

    if(text == '/help' or text == '/help@PygrameirosBot'):
        print(username + " usou o comando /help em: " + time)
        bot.sendMessage(chat_id, 'Olá, sou o PygrameirosBot!\nSegue a minha lista de comandos:\n/info -> Informações do grupo\n/link -> Link do grupo')

MessageLoop(bot, handle).run_as_thread()
while 1:
    time.sleep(10)
