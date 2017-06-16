import telepot
import time
from datetime import datetime
from telepot.loop import MessageLoop

now = datetime.now()
bot = telepot.Bot(input('TOKEN> '))
updates = bot.getUpdates()
print(updates)

print("Bot inicializado!")

def welcome(msg): #AJUSTAR AS BOAS-VINDAS
	chat_id = telepot.glance(msg)

	if ('new_chat_member' in msg):
		new_member = msg['new_chat_member']['first_name']
	#if(content_type == 'new_chat_member'):
		get_bot_name = bot.getMe()
		bot_name = get_bot_name['first_name']
		#bot_username = '@{}'.format(get_bot_name['username'])
		if(new_member == bot_name):
			bot.sendMessage(chat_id, 'Olá, sou o PygrameirosBot!')
		else:
			#bot.sendMessage(chat_id,'Seja bem vindo ao Pygrameiros, '+new_member+'!')
			welcome = open('welcome.txt', 'r')
			welcome = welcome.read()
			bot.sendMessage(msg['chat']['id'], welcome)

def set_welcome(msg):
	try:
		text = str(msg['text'])
	except:
		text = ''
	if(text.startswith('/welcome')):
		#new_member = msg['new_chat_member']['first_name']

		first_name = str(msg['from']['first_name'])
		text = text.replace("$user", first_name)
		user_id = msg['from']['id']
		admins = bot.getChatAdministrators(msg['chat']['id'])
		adm_list = [adm['user']['id'] for adm in admins]
		if (user_id in adm_list):
			text = text.replace("/welcome ", "")
			welcome = open('welcome.txt', 'w')
			welcome.write(text)
			welcome.close()
			bot.sendMessage(msg['chat']['id'], "As mensagens de boas-vindas foram alteradas com sucesso!")

def goodbye(msg):
	chat_id = telepot.glance(msg)

	if ('left_chat_member' in msg):
		left_member = msg['left_chat_member']['first_name']
		#bot.sendMessage(chat_id,'Seja bem vindo ao Pygrameiros, '+new_member+'!')
		#welcome = open('welcome.txt', 'r')
		#welcome = welcome.read()
		bot.sendMessage(chat_id, 'Bye')

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
			rules = open('rules.txt', 'w')
			rules.write(text)
			rules.close()
			bot.sendMessage(msg['chat']['id'], "As novas regras foram salvas com sucesso!")

	if(text.startswith('/regras')):
		rules = open('rules.txt', 'r')
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

	if(text == '/start' or text == '/start@PygrameirosBot'):
		users_register.write(str("log [" + day + "/" + month + "/" + year + "][" + hour + ":" + minute + ":" + second + "]"))
		users_register.write(str(" | Username: " + str(msg['from']['username']) + " | ID: " + str(msg['from']['id']) + " | Comando usado: " + text + "\n"))
		users_register.close()
		print("@"+ str(msg['from']['username']) + " Iniciou o Bot - Dados salvos!")

	else:
		log.write(str("log [" + day + "/" + month + "/" + year + "][" + hour + ":" + minute + ":" + second + "]"))
		log.write(str(" | Username: " + str(msg['from']['username']) + " | ID: " + str(msg['from']['id']) + " | Comando usado: " + text + " | ChatType: " + str(chat_type) + " | Chat ID: " + str(chat_id) + "\n"))
		log.close()
		print("@"+ str(msg['from']['username']) + " Usou o Bot! - Dados salvos!")

def commands(msg):
	content_type, chat_type, chat_id = telepot.glance(msg)
	try:
		text = str(msg['text'])
	except:
		text = ''

	if(chat_type == 'private'):
		if(text == '/start' or text == '/start@PygrameirosBot'):
			bot.sendMessage(chat_id, "Olá, eu sou o PygrameirosBot!\nFui criado pela galera do Pygrameiros para te ajudar a administrar teu grupo!")
			log(msg)

	if(chat_type != 'private'):
		if(text == '/start' or text == '/start@PygrameirosBot'):
			bot.sendMessage(chat_id, "Oi! Por favor, inicie uma conversa privada. Bots funcionam apenas desta forma.")
			log(msg)

	if(text == '/info' or text == '/info@PygrameirosBot'):
		bot.sendMessage(str(chat_id), str("ID INFO \n\n NOME: " + str(msg['from']['username']) + " \n ID: " + str(msg['from']['id']) + " \n NOME DO GRUPO: " + str(msg['chat']['title']) + " \n ID GROUP: " + str(chat_id)))

	if(text == '/link' or text == '/link@PygrameirosBot'):
		bot.sendMessage(chat_id, 'Nosso link é: https://goo.gl/m0h2eQ')
		log(msg)

	if(text == '/ajuda' or text == '/help@PygrameirosBot'):
		bot.sendMessage(chat_id, 'Olá, sou o PygrameirosBot!\nSegue a minha lista de comandos:\n/info -> Informações do grupo\n/link -> Link do grupo')
		log(msg)
	###ADMINS COMMANDS###
	if(text == '/ban' or text == '/ban@PygrameirosBot'):
		user_id = msg['from']['id']
		user = msg['reply_to_message']['from']['first_name']
		reply_id = msg['reply_to_message']['from']['id']
		admins = bot.getChatAdministrators(chat_id)
		adm_list = [adm['user']['id'] for adm in admins]
		if (user_id in adm_list):
			if reply_id not in adm_list:
				bot.sendMessage(chat_id, "*%s* foi banido" %(user), parse_mode="Markdown")
				bot.kickChatMember(chat_id, reply_id)
			else:
				bot.sendMessage(chat_id, '*%s* é adm do grupo' % (user), "Markdown" )
		else:
			bot.sendMessage(chat_id, 'Apenas administradores podem usar este comando.')

		if(text == '/kick' or text == '/kick@PygrameirosBot'):
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
					bot.sendMessage(chat_id, '*%s* é adm do grupo' % (user), "Markdown" )
			else:
				bot.sendMessage(chat_id, 'Apenas administradores podem usar este comando.')

def handle(msg):
	log(msg)
	commands(msg)
	welcome(msg)
	set_welcome(msg)
	rules(msg)

MessageLoop(bot, handle).run_as_thread()
while 1:
    time.sleep(10)
