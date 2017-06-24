
import telepot
import time
import logging
import sys
from datetime import datetime
from telepot.loop import MessageLoop

now = datetime.now()

TOKEN = sys.argv[1]
bot = telepot.Bot(TOKEN) #fazendo a comunicação com a API do Telegram via TOKEN
updates = bot.getUpdates()
print(updates)

print("Bot inicializado!")

def welcome(msg):
	chat_id = telepot.glance(msg)
	try:
		text = str(msg['text'])
	except:
		text = ''

	if(text.startswith('/welcome')):
		first_name = str(msg['from']['first_name'])
		user_id = msg['from']['id']
		admins = bot.getChatAdministrators(msg['chat']['id'])
		adm_list = [adm['user']['id'] for adm in admins]
		if (user_id in adm_list):
			text = text.replace("/welcome ", "")
			welcome = open('welcome.txt', 'w')
			welcome.write(text)
			welcome.close()
			bot.sendMessage(msg['chat']['id'], "As mensagens de boas-vindas foram alteradas com sucesso!")
		else:
			bot.sendMessage(msg['chat']['id'], "Comando restrito aos administradores.")

	if ('new_chat_member' in msg):
		user_first_name = msg['new_chat_member']['first_name']
		user_last_name = msg['new_chat_member']['last_name']
		#username = '@{}'.format(msg['new_chat_member']['username'])
		get_bot_name = bot.getMe()
		bot_name = get_bot_name['first_name']
		#bot_username = '@{}'.format(get_bot_name['username'])
		if(user_first_name == bot_name):
			bot.sendMessage(chat_id, 'Olá, sou o PygrameirosBot!')
		else:
			welcome = open('welcome.txt', 'r')
			welcome = welcome.read()
			welcome = welcome.replace("$name", user_first_name)
			welcome = welcome.replace('$surname', user_last_name)
			#welcome = welcome.replace('$username', username)
			bot.sendMessage(msg['chat']['id'], welcome)

def rules(msg):
	try:
		text = str(msg['text'])
	except:
		text = ''
	if(text.startswith('/defregras')):
		user_id = msg['from']['id']
		admins = bot.getChatAdministrators(msg['chat']['id'])
		adm_list = [adm['user']['id'] for adm in admins]
		if (user_id in adm_list):
			text = text.replace("/defregras ", "")
			rules = open('regras.txt', 'w')
			rules.write(text)
			rules.close()
			bot.sendMessage(msg['chat']['id'], "As novas regras foram salvas com sucesso!")
		else:
			bot.sendMessage(msg['chat']['id'], "Comando restrito aos administradores.")

	if(text.startswith('/regras')):
		rules = open('regras.txt', 'r')
		rules = rules.read()
		bot.sendMessage(msg['chat']['id'], rules)

def log(msg):
	day = str(now.day)
	month = str(now.month)
	year = str(now.year)
	hour = str(now.hour)
	minute = str(now.minute)
	second = str(now.second)

	content_type, chat_type, chat_id = telepot.glance(msg)
	log = open('log.txt', 'a')
	users_register = open('users_register.txt', 'a')
	try:
		text = str(msg['text'])
	except:
		text = ''

	if(text.startswith('/start')):
		logging.basicConfig(filename='users_register.log', filemode='w', level=logging.INFO)
		logging.info(str(" log [" + day + "/" + month + "/" + year + "][" + hour + ":" + minute + ":" + second + "]"))
		logging.info(str("| Username: " + str(msg['from']['username']) + " | ID: " + str(msg['from']['id']) + " | Comando usado: " + text + "\n"))
		"""users_register.close()
		print("@"+ str(msg['from']['username']) + " Iniciou o Bot - Dados salvos!")"""

	elif(text.startswith('/') and text != '/start'):
		logging.basicConfig(filename='log.log', filemode='w', level=logging.INFO)
		logging.info(str(" log [" + day + "/" + month + "/" + year + "][" + hour + ":" + minute + ":" + second + "]"))
		logging.info(str("| Username: " + str(msg['from']['username']) + " | ID: " + str(msg['from']['id']) + " | Comando usado: " + text + " | ChatType: " + str(chat_type) + " | Chat ID: " + str(chat_id) + "\n"))
		print("@"+ str(msg['from']['username']) + " Usou o Bot! - Dados salvos!")

def commands(msg):
	content_type, chat_type, chat_id = telepot.glance(msg)
	try:
		text = str(msg['text'])
	except:
		text = ''

	if(chat_type == 'private'):
		if(text.startswith('/start')):
			bot.sendMessage(chat_id, "Olá, eu sou o PygrameirosBot!\nFui criado pela galera do Pygrameiros para te ajudar a administrar teu grupo!")
			log(msg)

	if(chat_type != 'private'):
		if(text.startswith('/start')):
			bot.sendMessage(chat_id, "Oi! Por favor, inicie uma conversa privada. Bots funcionam apenas desta forma.")
			log(msg)

	if(text.startswith('/info')):
		bot.sendMessage(str(chat_id), str("ID INFO \n\n NOME: " + str(msg['from']['username']) + " \n ID: " + str(msg['from']['id']) + " \n NOME DO GRUPO: " + str(msg['chat']['title']) + " \n ID GROUP: " + str(chat_id)))

	if(text.startswith('/link')):
		bot.sendMessage(chat_id, '[Pygrameiros](https://t.me/joinchat/AAAAAEOnjcIiD2WH_TD8Vg)', parse_mode="Markdown")
		log(msg)

	if(text.startswith('/ajuda')):
		bot.sendMessage(chat_id, 'Olá, sou o PygrameirosBot!\nSegue a minha lista de comandos:\n/info -> Informações do grupo\n/link -> Link do grupo')
		log(msg)

	if(text.startswith('/leave')):
		chat_id = msg['chat']['id']
		user_id = msg['from']['id']
		bot.kickChatMember(chat_id, user_id)
	###ADMINS COMMANDS###
	if(text.startswith('/ban') or text.startswith('/kick')):
		user_id = msg['from']['id']
		user = msg['reply_to_message']['from']['first_name']
		reply_id = msg['reply_to_message']['from']['id']
		admins = bot.getChatAdministrators(chat_id)
		adm_list = [adm['user']['id'] for adm in admins]
		if (user_id in adm_list):
			if reply_id not in adm_list:
				bot.sendMessage(chat_id, "*%s* foi retirado do grupo." %(user), parse_mode="Markdown")
				bot.kickChatMember(chat_id, reply_id)
			else:
				bot.sendMessage(chat_id, '*%s* é um dos administradores. Não posso remover administradores.' % (user), "Markdown" )
		else:
			bot.sendMessage(chat_id, 'Apenas administradores podem usar este comando.')

def handle(msg):
	try:
		text = msg['text']
	except:
		text = ''

	print(text)
	log(msg)
	commands(msg)
	welcome(msg)
	rules(msg)


MessageLoop(bot, handle).run_as_thread()
while 1:
    time.sleep(10)
