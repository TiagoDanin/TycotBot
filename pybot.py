import telepot
import time
from datetime import datetime

now = datetime.now()
bot = telepot.Bot(str(input("TOKEN> ")))
updates = bot.getUpdates()
print(updates)

print("Bot inicializado!")

def contact_admin(msg):
    bot.sendMessage(msg['chat']['id'], input("> "))


def handle(msg): #Ainda faltam alguns dados a serem adicionados#
    #Dados do usuário/bot
    user_id = float(msg['from']['id']) #ID do usuário ou bot
    first_name = str(msg['from']['first_name']) #Primeiro nome
    language_code = str(msg['from']['language_code']) #idioma do usuário
    #Dados do Chat
    chat_id = float(msg['chat']['id']) #ID do chat
    chat_type = str(msg['chat']['type']) #Tipo do bate-papo (privado, grupo...)

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

    users = open('users-register.txt', 'a')
    log = open('log_comands.txt', 'a')


    if text == '/start':
        if chat_type == 'private':
            print(username + " iniciou o bot!")
            bot.sendMessage(chat_id, "Olá, eu sou o Pybot!\n")
            bot.sendMessage(chat_id, "Você deseja entrar em contato com os admins do Pygrameiros?")
            while True: #Parei aqui (ajustar depois)
                if text == 'sim':
                    bot.sendMessage(186027472, "Consulte o Pybot!")
                    contact_admin(msg)
                else:
                    text = false
        #Salvando os dados no arquivo users
            users.write(str("log [" + day + "/" + month + "/" + year + "][" + hour + ":" + minute + ":" + second + "]"))
            users.write(str(" | Username: " + username + " | ID: " + str(user_id) + " | Comando usado: " + text + " | Chat: " + chat_type + "\n"))
            users.close()
            print("@"+username + " ("+ first_name + " " + last_name + ") " + " Iniciou o Bot - Dados salvos!")
        elif chat_type == 'supergroup':
            bot.sendMessage(chat_id, "Por favor, inicie uma conversa no privado!", reply_to_message_id=message_id)
    elif text == '/id':
        bot.sendMessage(chat_id, str("Pybot - Info ID \n\n *Nome:* " + username + " \n *ID:* " + user_id + " \n *Nome do Grupo:* " + chat_title + " \n *Id Group:* " + chat_id) , parse_mode="Markdown",reply_to_message_id=message_id)
        log.write(str("log [" + day + "/" + month + "/" + year + "][" + hour + ":" + minute + ":" + second + "]"))
        log.write(str(" | Username: " + username + " | ID: " + user_id + " | Comando usado: " + text + " | ChatType: " + chat_type + " | Chat ID: " + chat_id + "\n"))
        log.close()
        print("@"+username + " ("+ first_name + " " + last_name + ") " + " Usou o Bot! - Dados salvos!")

bot.message_loop(handle)
while 1:
    pass
