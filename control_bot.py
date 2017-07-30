import telepot
import logging
import sql
from datetime import datetime
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton


class control:

	day_date_hour = datetime.now().strftime('%c')


	def __init__(self, msg, bot):

		try:
			self.bot = bot
			self.msg = msg
			self.user, self.user_id =  msg['from']['username'] , msg['from']['id']
			self.content_type, self.chat_type, self.chat_id = telepot.glance(msg)
			self.admins = self.bot.getChatAdministrators(self.chat_id)
			first_name = msg['from']['first_name']

			#get admin
			self.adm_list = [adm['user']['id'] for adm in self.admins]
	
		except:
			pass
		try:
			self.text = msg['text']
		except:
			self.text = ''

		

	def commands(self):

		if self.chat_type == 'private':

			if self.text.startswith('/start'):
				self.bot.sendMessage(self.chat_id, ('Olá, eu sou o Tycot!\nFui criado pela galera do Pygrameiros para te ajudar a administrar teu grupo!'))
			self.log()
            
		elif self.text.startswith('/start'):
			self.bot.sendMessage(self.chat_id, ("Oi! Por favor, inicie uma conversa privada."
                                                " Bots funcionam apenas desta forma."))
			self.log()

        
		try:
			if self.text.startswith('/info'):
				if self.chat_type == 'private':
                    
					self.bot.sendMessage(chat_id=self.chat_id, parse_mode='Markdown', text='''*ID INFO*\n`NOME`: {0}\n`ID`: {1}'''.format(self.user, self.user_id))
				else:

					info_chat = self.msg['chat']['title']

					self.bot.sendMessage(chat_id=self.user_id, parse_mode='Markdown',text='*ID INFO*\n`NOME`: {0}\n`ID`: {1}\n`NOME DO GRUPO`: {2}\n`ID GROUP`: {3}'.format(self.user, self.user_id, info_chat, self.chat_id))

			if self.text.startswith('/link'):
				self.bot.sendMessage(self.user_id, parse_mode='Markdown', text='[Pygrameiros](https://t.me/joinchat/AAAAAEOnjcIiD2WH_TD8Vg)')
				self.log()

			if self.text.startswith('/ajuda'):
				self.bot.sendMessage(self.user_id, ('''
							Olá, sou o Tycot!
							Segue minha lista de comandos:
							/info -> informações do grupo
							/link -> link do grupo
							/regras -> regras do grupo
							/leave -> sair do grupo
														'''))
				self.log()

		except:
			self.bot.sendMessage(self.chat_id, 'Por favor, inicie uma conversa comigo e tente novamente.')

		if self.text.startswith('/leave'):
            
			self.bot.sendMessage(self.chat_id, "Tem certeza que deseja sair do grupo?\nEnvie 'sim' ou 'não'.")
            
			if(self.text == 'sim'):
				self.bot.kickChatMember(self.chat_id, self.user_id)
        

        	###  ADMINS COMMANDS  ###
		if(self.text.startswith('/ban')) or (self.text.startswith('/kick')):

			user = self.msg['reply_to_message']['from']['first_name']
			reply_id = self.msg['reply_to_message']['from']['id']            
			adm_list = [adm['user']['id'] for adm in self.admins]

			if self.user_id in adm_list:
                
				if reply_id not in adm_list:
					self.bot.sendMessage(self.chat_id, "*{user}* foi retirado do grupo.".format(user), parse_mode="Markdown")
					self.bot.kickChatMember(self.chat_id, reply_id)
				else:
					self.bot.sendMessage(self.chat_id, '*{}* é um dos administradores. Não posso remover administradores.'.format(user), parse_mode="Markdown")
			else:
				self.bot.sendMessage(self.chat_id, 'Apenas administradores podem usar este comando.')
    
		#warn falta alguns ajustes ainda.
		if self.text.startswith('/warn'):
			user = self.msg['reply_to_message']['from']['username']
			self.user_reply_id = self.msg['reply_to_message']['from']['id'] #Esse valor será usado para remover o warn pelo botão tbm na função keyboard que irar retornar o id quando pressionado...
			advs = int(sql.procurar(self.chat_id, user)[1])
			user1 = self.msg['reply_to_message']['from']['first_name']

			if (self.user_id in self.adm_list):
    				
				if self.user_reply_id not in self.adm_list:
					self.bot.sendMessage(self.chat_id,'{user} *has been warned* ({advs}/3).'.format(user=user1, advs=advs+1), parse_mode="Markdown", reply_markup=self.keyboard())
					sql.advertir(self.chat_id, user)
					if advs >= 3:
						self.bot.sendMessage(self.chat_id, '*{}* expulso por atingir o limite de advertencias.'.format(user1), parse_mode="Markdown")
						self.bot.kickChatMember(self.chat_id, self.user_reply_id)
						sql.delete(self.chat_id, user)
					else:
						pass

				else:
					self.bot.sendMessage(self.chat_id, '*{}* é um dos administradores. Não posso advertir administradores.'.format(user1), parse_mode="Markdown")
			else:
				self.bot.sendMessage(self.chat_id, 'Apenas administradores podem usar este comando.')

		#warn falta alguns ajustes ainda
		if (self.text.startswith('/unwarn')): #or (self.msg['data'] == 'removewarn'):

			user = self.msg['reply_to_message']['from']['username']
			user1 = self.msg['reply_to_message']['from']['first_name']
			self.user_reply_id = self.msg['reply_to_message']['from']['id']
			advs = int(sql.procurar(self.chat_id, user)[1])

			if self.user_id in self.adm_list:
						
				if self.user_reply_id not in self.adm_list:
					self.bot.sendMessage(self.chat_id,'*{}* batizado.'.format(user1), parse_mode='Markdown')
					sql.desadvertir(self.chat_id, user, advs-1)
				else:
					self.bot.sendMessage(self.chat_id,'administradores não possuem advertencias.')

			else:
				self.bot.sendMessage(self.chat_id, 'você ainda não pode batizar alguém, torne-se padre antes.')


	def log(self):

		if(self.text.startswith('/start')):
			logging.basicConfig(filename='users_register.log', filemode='w', level=logging.INFO)
			logging.info("log [{}]".format(self.day_date_hour))

			logging.info(" | Username: {} | ID: {} | Comando usado: {}\n".format(self.user,self.user_id, self.text))

			print("@{} Iniciou o Bot - Dados salvos!".format(self.user))

		elif(self.text.startswith('/') and self.text != '/start'):
			logging.basicConfig(filename='log.log', filemode='w', level=logging.INFO)
			logging.info("log [{}]" .format(self.day_date_hour))

			logging.info(" | Username: {} | ID: {} | Comando usado: {}\n".format(self.user,self.user_id, self.text))

			print("@{} Usou o Bot - Dados salvos!".format(self.user))



	def goodbye(self):
        
		if('left_chat_member' in self.msg):
			user_first_name = str(self.msg['left_chat_member']['first_name'])
			self.bot.sendMessage(self.chat_id, "Tchau, {}".format(user_first_name))
			self.bot.sendVideo(self.chat_id, "https://media.giphy.com/media/l3V0gpbjA6fD7ym9W/giphy.mp4")
    

	def rules(self):

		if(self.text.startswith('/defregras')):
            
			adm_list = [adm['user']['id'] for adm in self.admins]
			if (self.user_id in adm_list):
				text = self.text.replace("/defregras ", "")
                
				with open('regras.txt', 'a') as rules:
					rules.write(text)

				return self.bot.sendMessage(self.chat_id, "As novas regras foram salvas com sucesso!")
			else:
				return self.bot.sendMessage(self.chat_id, "Comando restrito aos administradores.")

		if(self.text.startswith('/regras')):
            
			with open('regras.txt', 'r') as rules:
				rules = rules.read()
			return self.bot.sendMessage(self.chat_id, rules)

    
	def welcome(self):

		if self.text.startswith('/welcome'):
                        
			if self.user_id in self.adm_list:
				text = self.text.replace("/welcome ", "")

				with open('welcome.txt', 'w') as welcome:
					welcome.write(text[1])

				self.bot.sendMessage(self.chat_id, "As mensagens de boas-vindas foram alteradas com sucesso!")
			else:
				self.bot.sendMessage(self.msg['chat']['id'], "Comando restrito aos administradores.")

		if 'new_chat_member' in self.msg:
            
			user_first_name = str(self.msg['new_chat_member']['first_name'])
			get_bot_name = self.bot.getMe()
			bot_name = get_bot_name['first_name']

			if(user_first_name == bot_name):
				self.bot.sendMessage(self.chat_id, 'Olá, sou o Tycot!')
				sql.criar_table(self.chat_id)
			else:
                    
				with open('welcome.txt', 'r') as welcome:
					welcome = welcome.read()
					welcome = welcome.replace('$name', user_first_name)
					self.bot.sendMessage(self.chat_id, welcome)
					sql.inserir(self.chat_id, self.msg['new_chat_member']['username'])


	def keyboard(self):

		if self.text == '/warn': 
			return InlineKeyboardMarkup(inline_keyboard=[
                            [InlineKeyboardButton(text="Remove warn", callback_data='d')]
                    ])