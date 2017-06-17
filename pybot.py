'''
    * Install python3+++
    * Use Teleport API
    * Configure seu bot
'''

import telepot
import time
from datetime import datetime
from telepot.loop import MessageLoop

now = datetime.now()
bot = telepot.Bot("435414159:AAGGST7VegBfad_3MIVjoIe53FDGkOuMfG0")
updates = bot.getUpdates()
print(updates)

print("Bot inicializado!")

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

    day = str(now.day)
    month = str(now.month)
    year = str(now.year)
    hour = str(now.hour)
    minute = str(now.minute)
    second = str(now.second)
    time = (hour+':'+minute+':'+second+' -> '+day+'/'+month+'/'+year)

    users = open('users-register.txt', 'a')
    log = open('log_comands.txt', 'a')

    #boas-vindas
    #corrigir o bug que ele dá boas vindas a si mesmo
    if( content_type == 'new_chat_member'):
        if('new_chat_member' == "@Dialup_bot"):
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


    if text == '/ban': #TheGrillo que fez, corrigir nome das variáveis depois#
        print(username + " usou o comando /ban em: " + time)
        """nome = msg['reply_to_message_id']['from']['first_name'] reply_to_message_id = msg['reply_to_message']['from']['id']
        admins = bot.getChatAdministrators(chat_id)
        adm_list = [adm['user']['id']
        for adm in admins]
        if (chat_id in adm_list):
            if reply_to_message_id not in adm_list:
                bot.sendMessage(chat_id, "*%s* foi banido" %(nome), parse_mode="Markdown") bot.kickChatMember(chat_id, reply_id) else: bot.sendMessage(chat_id, '*%s* é adm do grupo' %(nome), "Markdown" ) elif from_id not in adm_list: bot.sendMessage(chat_id, 'não quelu 😆')"""

MessageLoop(bot, handle).run_as_thread()
while 1:
    time.sleep(10)
