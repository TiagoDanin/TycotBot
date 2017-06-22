#importando as libs necessárias para o funcionamento do bot
import telepot #framework utilizada
import time
from datetime import datetime
from telepot.loop import MessageLoop

now = datetime.now() #setando o horário no momento
bot = telepot.Bot(input('TOKEN> ')) #fazendo a comunicação com a API do Telegram via TOKEN
updates = bot.getUpdates() #Recebendo updates de mensagens recebidas enquanto o bot estava offline
print(updates) #exibindo os updates

print("Bot inicializado!") #mensagem exibida ao iniciar o bot

def welcome(msg): #função de boas-vindas
	chat_id = telepot.glance(msg) #definindo o chat_id
	#tratamento para o text; devido a alguns erros, tive que definir desta forma
	try:
		text = str(msg['text'])
	except:
		text = ''

	if(text.startswith('/welcome')): #caso o text inicie com /welcome...
		first_name = str(msg['from']['first_name']) #pegando o primeiro nome do usuário que enviou o 'text'
		user_id = msg['from']['id'] #pegando o ID do usuário que enviou o 'text'
		admins = bot.getChatAdministrators(msg['chat']['id']) #pegando os admins do grupo
		adm_list = [adm['user']['id'] for adm in admins] #rodando a lista dos admins...
		if (user_id in adm_list): #caso o ID do usuário esteja na lista dos admins, este código entra em execução
			text = text.replace("/welcome ", "") #retirando o '/welcome' do início do 'text'...
			welcome = open('welcome.txt', 'w') #abrindo o arquivo onde é salvo as boas-vindas
			welcome.write(text) #gravando o 'text' no arquivo que abrimos
			welcome.close() #fechando o arquivo
			bot.sendMessage(msg['chat']['id'], "As mensagens de boas-vindas foram alteradas com sucesso!") #o bot envia uma mensagem que foi concluido com sucesso ao grupo
		else: #caso o usuário não esteja na lista de admins...
			bot.sendMessage(msg['chat']['id'], "Comando restrito aos administradores.") #o bot envia uma mensagem falando que o usuário não tem poderes para tal comando

	if ('new_chat_member' in msg): #caso nas mensagens do grupo esteja um novo membro...
		user_first_name = msg['new_chat_member']['first_name'] #pegando o primeiro nome do novo membro
		user_last_name = msg['new_chat_member']['last_name'] #pegando o último nome do novo membro
		#username = '@{}'.format(msg['new_chat_member']['username'])
		get_bot_name = bot.getMe() #pegando os dados do bot
		bot_name = get_bot_name['first_name'] #pegando o primeiro nome do bot
		#bot_username = '@{}'.format(get_bot_name['username'])
		if(user_first_name == bot_name): #caso o o novo membro seja o próprio bot...
			bot.sendMessage(chat_id, 'Olá, sou o PygrameirosBot!') #o bot envia uma mensagem de "hello"
		else: #caso não seja o bot o novo membro...
			welcome = open('welcome.txt', 'r') #abrindo o arquivo de boas-vindas
			welcome = welcome.read() #salvando o arquivo numa string
			welcome = welcome.replace("$name", user_first_name) #trocando $name pelo primeiro nome do novo membro
			welcome = welcome.replace('$surname', user_last_name) #trocando o $surname pelo último nome do novo membro
			#welcome = welcome.replace('$username', username)
			bot.sendMessage(msg['chat']['id'], welcome) #enviando as mensagens de boas-vindas ao novo membro

def rules(msg): #função responsável pela definição e exibição das regras
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
	#definindo a data e horário
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
	#caso seja usado o comando '/start', é salvo um log de quando o usuário iniciou o bot
	if(text.startswith('/start')):
		users_register.write(str("log [" + day + "/" + month + "/" + year + "][" + hour + ":" + minute + ":" + second + "]"))
		users_register.write(str(" | Username: " + str(msg['from']['username']) + " | ID: " + str(msg['from']['id']) + " | Comando usado: " + text + "\n"))
		users_register.close()
		print("@"+ str(msg['from']['username']) + " Iniciou o Bot - Dados salvos!")

	else:
		log.write(str("log [" + day + "/" + month + "/" + year + "][" + hour + ":" + minute + ":" + second + "]"))
		log.write(str(" | Username: " + str(msg['from']['username']) + " | ID: " + str(msg['from']['id']) + " | Comando usado: " + text + " | ChatType: " + str(chat_type) + " | Chat ID: " + str(chat_id) + "\n"))
		log.close()
		print("@"+ str(msg['from']['username']) + " Usou o Bot! - Dados salvos!")

def commands(msg): #função para interação com membros de grupos
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

def handle(msg): #função principal, responsável por rodar todas as demais
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
