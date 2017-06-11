import telepot
import time
from datetime import datetime
from telepot.loop import MessageLoop
import json
from html import escape

now = datetime.now()
bot = telepot.Bot("TOKEN")
updates = bot.getUpdates()
print(updates)

print("Bot inicializado!")


def handle(msg): #Ainda faltam alguns dados a serem adicionados#
    #Dados do usuário/bot
    user_id = float(msg['from']['id']) #ID do usuário ou bot
    first_name = str(msg['from']['first_name']) #Primeiro nome
    #Dados do Chat
    chat_id = float(msg['chat']['id']) #ID do chat
    chat_type = str(msg['chat']['type']) #Tipo do bate-papo (privado, grupo...)


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
        username = str(msg['from']['username'])
    except:
        username = ""
    try:
        last_name = str(msg['from']['last_name'])
    except:
        last_name = ""
    try:
        new_member = msg['new_chat_members']['first_name'+ ' last_name']
    except:
        new_member = ''

    day = str(now.day)
    month = str(now.month)
    year = str(now.year)
    hour = str(now.hour)
    minute = str(now.minute)
    second = str(now.second)
    time = (hour+':'+minute+':'+second+' -> '+day+'/'+month+'/'+year)

    users = open('users-register.txt', 'a')
    log = open('log_comands.txt', 'a')

    #welcome
    if(content_type == 'new_chat_members'):
         bot.sendMessage(chat_id,'welcome')

    if(chat_type == 'private'):
        if(text == '/start' or '/start@PygrameirosBot'):
            print(username + " iniciou o bot em: " + time)
            bot.sendMessage(chat_id, "Olá, eu sou o Pybot!\nFui criado pela galera do Pygrameiros para te ajudar a administrar teu grupo!")
            #Salvando os dados no arquivo users
            users.write(str("log [" + day + "/" + month + "/" + year + "][" + hour + ":" + minute + ":" + second + "]"))
            users.write(str(" | Username: " + username + " | ID: " + str(user_id) + " | Comando usado: " + text + " | Chat: " + chat_type + "\n"))
            users.close()
            print("@"+username + " ("+ first_name + " " + last_name + ") " + " Iniciou o Bot - Dados salvos!")
    elif(text == '/info' or text == '/info@PygrameirosBot'):
        bot.sendMessage(str(chat_id), str("ID INFO \n\n NOME: " + username + " \n ID: " + str(user_id) + " \n NOME DO GRUPO: " + chat_title + " \n ID GROUP: " + str(chat_id)) ,reply_to_message_id=str(message_id))
        log.write(str("log [" + day + "/" + month + "/" + year + "][" + hour + ":" + minute + ":" + second + "]"))
        log.write(str(" | Username: " + username + " | ID: " + str(user_id) + " | Comando usado: " + text + " | ChatType: " + chat_type + " | Chat ID: " + str(chat_id) + "\n"))
        log.close()
        print("@"+username + " ("+ first_name + " " + last_name + ") " + " Usou o Bot! - Dados salvos!")

    elif(text == '/members'):
        members = getChatMembersCount()
        bot.sendMessage(chat_id, members)
    """elif texto == '/ban': #TheGrillo que fez, corrigir nome das variáveis depois#
        nome = msg['reply_to_message_id']['from']['first_name'] reply_to_message_id = msg['reply_to_message']['from']['id']
        admins = bot.getChatAdministrators(chat_id)
        adm_list = [adm['user']['id']
        for adm in admins]
        if (chat_id in adm_list):
            if reply_to_message_id not in adm_list:
                bot.sendMessage(chat_id, "*%s* foi banido" %(nome), parse_mode="Markdown") bot.kickChatMember(chat_id, reply_id) else: bot.sendMessage(chat_id, '*%s* é adm do grupo' %(nome), "Markdown" ) elif from_id not in adm_list: bot.sendMessage(chat_id, 'não quelu 😆')"""

MessageLoop(bot, handle).run_as_thread()
while 1:
    time.sleep(10)
