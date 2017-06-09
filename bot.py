import telepot
import time
from datetime import datetime

now = datetime.now()
bot = telepot.Bot(str(input("Insira o token> ")))

def handle(msg):

    uid = str(msg['from']['id'])
    pnome = str(msg['from']['first_name'])#Primeiro nome
    chat_id = msg['chat']['id']#id do grupo
    chat_type = msg['chat']['type']
    
    try:
        chat_title = str(msg['chat']['title'])
    except:
        chat_title = ''
    try:
        texto = str(msg['text'])
    except:
        texto = ''
    try:
        ntexto = texto.spli(' ')
    except:
        ntexto = ''
    try:
        nick = msg['from']['username']#username, @username
    except:
        nick = ''
    try:
        new_member = msg['new_chat_member']['first_name']
    except:
        new_member = ''
    try:
    	msgid = msg['message_id']#id da msg
    except:
    	msgid =''

    # Variaveis cronologicas
    dia = str(now.day)
    mes = str(now.month)
    ano = str(now.year)
    hora = str(now.hour)
    minut = str(now.minute)
    segundo = str(now.second)

    #Codigo - log do comandos
    users = open('users-register.txt', 'a')
    log = open('log_comands.txt', 'a')

    #Variaveis para funções
    ntexto = texto.split(' ')

    if texto == '/start':
        if chat_type == 'private':
            bot.sendMessage(chat_id, "Olá, eu sou o PygrameirosBot, fui criado pela galera do Pygrameiros para facilitar a administração do teu grupo! \n\n")
            users.write(str("log [" + dia + "/" + mes + "/" + ano + "][" + hora + ":" + minut + ":" + segundo + "]"))
            users.write(str(" | Username: " + nick + " | ID: " + str(uid) + " | Comando usado: " + texto + " | Chat: " + chat_type + "\n"))
            users.close()
            print(nick + " Iniciou o Bot - Dados salvos!")
        else:
            bot.sendMessage(chat_id, "Por favor inicie uma conversa no privado!", reply_to_message_id=msgid)
    elif texto == '/id':
        bot.sendMessage(chat_id, str("PygrameirosBot - Info ID \n\n *Nome:* " + nick + " \n *ID:* " + str(uid) + " \n *Nome do Grupo:* " + chat_title + " \n *Id Group:* " + str(chat_id)) , parse_mode="Markdown",reply_to_message_id=msgid)
        log.write(str("log [" + dia + "/" + mes + "/" + ano + "][" + hora + ":" + minut + ":" + segundo + "]"))
        log.write(str(" | Username: " + nick + " | ID: " + str(uid) + " | Comando usado: " + texto + " | ChatType: " + chat_type + " | Chat ID: " + str(chat_id) + "\n"))
        log.close()
        print(nick + " Usou o Bot - Log criado!")

time.sleep(2)
bot.message_loop(handle)
print("Bot Iniciado")
while 1:
    time.sleep(10)
