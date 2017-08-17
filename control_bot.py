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
			if 'username' in msg['from']:
				self.user = msg['from']['username']
			else:
				self.user = "[Sem username]"
			self.user_id = msg['from']['id']
			self.content_type, self.chat_type, self.chat_id = telepot.glance(msg)
			self.admins = self.bot.getChatAdministrators(self.chat_id)
			self.first_name = msg['from']['first_name']

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
				self.bot.sendMessage(
					self.chat_id,
					('Olá, eu sou o Tycot!\nFui criado pela galera do Programeiros para te ajudar'
					' a administrar teu grupo!')
				)
			self.log()

		elif self.text.startswith('/start'):
			self.bot.sendMessage(
				self.chat_id,
				('Oi! Por favor, inicie uma conversa privada.'
				' Bots funcionam apenas desta forma.'),
				reply_markup=InlineKeyboardMarkup(
					inline_keyboard=[
						[
							InlineKeyboardButton(
								text='Inicia uma conversa',
								url='https://telegram.me/TycotBot'
							)
						]
					]
				)
			)
			self.log()


		try:
			if self.text.startswith('/info'):
				if self.chat_type == 'private':
					self.bot.sendMessage(
						chat_id=self.chat_id,
						parse_mode='HTML',
						text='''<b>ID INFO</b>\n<code>NOME</code>: {0}\n<code>ID</code>: {1}'''.format(
							self.first_name,
							self.user_id
						)
					)
				else:
					info_chat = self.msg['chat']['title']
					self.bot.sendMessage(
						chat_id=self.user_id,
						parse_mode='HTML',
						text='<b>ID INFO</b>\n<code>NOME</code>: {0}\n<code>ID</code>: {1}\n<code>NOME DO GRUPO</code>: {2}\n<code>ID GROUP</code>: {3}'.format(
							self.user,
							self.user_id,
							info_chat,
							self.chat_id
						)
					)

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
			self.bot.sendMessage(
				self.chat_id,
				'Por favor, inicie uma conversa comigo e tente novamente.'
			)

		if self.text.startswith('/leave'):

			self.bot.kickChatMember(self.chat_id, self.user_id)


		###  ADMINS COMMANDS  ###
		if(self.text.startswith('/ban')) or (self.text.startswith('/kick')):

			first_name_reply = self.msg['reply_to_message']['from']['first_name']
			reply_id = self.msg['reply_to_message']['from']['id']
			adm_list = [adm['user']['id'] for adm in self.admins]

			if self.user_id in adm_list:

				if reply_id not in adm_list:
					self.bot.sendMessage(
						self.chat_id,
						'<b>{user}</b> foi retirado do grupo.'.format(first_name_reply),
						parse_mode='HTML'
					)
					self.bot.kickChatMember(self.chat_id, reply_id)
					try:
						sql.delete(self.chat_id, reply_id)
					except:
						pass
				else:
					self.bot.sendMessage(
						self.chat_id,
						'<b>{}</b> é um dos administradores. Não posso remover administradores.'.format(first_name_reply),
						parse_mode='HTML'
					)
			else:
				self.bot.sendMessage(self.chat_id, 'Apenas administradores podem usar este comando.')

		# warn falta alguns ajustes ainda.
		if self.text.startswith('/warn'):
			first_name_reply = self.msg['reply_to_message']['from']['first_name']
			self.user_reply_id = self.msg['reply_to_message']['from']['id'] #Esse valor será usado para remover o warn pelo botão tbm na função keyboard que irar retornar o id quando pressionado...
			try:
				advs = int(sql.procurar(self.chat_id, self.user_reply_id)[1])
			except:
				sql.inserir(self.chat_id, self.user_reply_id)
				advs = int(sql.procurar(self.chat_id, self.user_reply_id)[1])

			if (self.user_id in self.adm_list):

				if self.user_reply_id not in self.adm_list:
					self.bot.sendMessage(
						self.chat_id,
						'{user} <b>has been warned</b> ({advs}/3).'.format(
							user=first_name_reply, advs=advs+1
						),
						parse_mode='HTML',
						reply_markup=self.keyboard()
					)
					sql.advertir(self.chat_id, self.user_reply_id)
					if advs >= 3:
						self.bot.sendMessage(
							self.chat_id,
							'<b>{}</b> expulso por atingir o limite de advertencias.'.format(first_name_reply),
							parse_mode='HTML'
						)
						self.bot.kickChatMember(self.chat_id, self.user_reply_id)
						sql.delete(self.chat_id, self.user_reply_id)
					else:
						pass

				else:
					self.bot.sendMessage(
						self.chat_id,
						'<b>{}</b> é um dos administradores. Não posso advertir administradores.'.format(user1),
						parse_mode='HTML'
					)
			else:
				self.bot.sendMessage(
					self.chat_id,
					'Apenas administradores podem usar este comando.'
				)

		# warn falta alguns ajustes ainda
		if (self.text.startswith('/unwarn')): #or (self.msg['data'] == 'removewarn'):
			first_name_reply = self.msg['reply_to_message']['from']['first_name']
			self.user_reply_id = self.msg['reply_to_message']['from']['id']
			try:
				advs = int(sql.procurar(self.chat_id, self.user_reply_id)[1])
			except:
				pass

			if self.user_id in self.adm_list:

				if self.user_reply_id not in self.adm_list:
					self.bot.sendMessage(
						self.chat_id,
						'<b>{}</b> perdoado.'.format(first_name_reply),
						parse_mode='HTML'
					)
					sql.desadvertir(self.chat_id, self.user_reply_id, advs)
				else:
					self.bot.sendMessage(self.chat_id,'Administradores não possuem advertências.')

			else:
				self.bot.sendMessage(self.chat_id, 'Haha')


	def log(self):

		if(self.text.startswith('/start')):
			logging.basicConfig(filename='.tmp/users_register.log', filemode='w', level=logging.INFO)
			logging.info("log [{}]".format(self.day_date_hour))

			logging.info(" | Username: {} | ID: {} | Comando usado: {}\n".format(self.user,self.user_id, self.text))

			print("@{} Iniciou o Bot - Dados salvos!".format(self.user))

		elif(self.text.startswith('/') and self.text != '/start'):
			logging.basicConfig(filename='.tmp/log.log', filemode='w', level=logging.INFO)
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

				with open('.tmp/regras' + str(self.chat_id) + '.txt', 'w') as rules:
					rules.write(text)

				return self.bot.sendMessage(
					self.chat_id,
					'As novas regras foram salvas com sucesso!'
				)
			else:
				return self.bot.sendMessage(
					self.chat_id,
					'Comando restrito aos administradores.'
				)

		if(self.text.startswith('/regras')):
			try:
				with open('.tmp/regras' + str(self.chat_id) + '.txt', 'r') as rules:
					rules = rules.read()
			except FileNotFoundError:
				rules = 'Sem regras!'
			return self.bot.sendMessage(self.chat_id, rules, parse_mode='HTML')

	def link(self):

		if(self.text.startswith('/deflink')):
			adm_list = [adm['user']['id'] for adm in self.admins]
			if (self.user_id in adm_list):
				text = self.text.replace("/deflink ", "")

				with open('.tmp/link' + str(self.chat_id) + '.txt', 'w') as link_:
					link_.write(text)

				return self.bot.sendMessage(
					self.chat_id,
					'O novo link foi salvou com sucesso!'
				)
			else:
				return self.bot.sendMessage(
					self.chat_id,
					'Comando restrito aos administradores.'
				)

		if(self.text.startswith('/link')):
			info_chat = self.msg['chat']['title']
			try:
				with open('.tmp/link' + str(self.chat_id) + '.txt', 'r') as link_:
					link_tg = link_.read()
			except FileNotFoundError:
				link_tg = 'Sem link!'
			link_msg = '<a href="' + str(link_tg) + '">' + str(info_chat) + '</a>'
			return self.bot.sendMessage(self.chat_id, link_msg, parse_mode='HTML')

	def welcome(self):

		if self.text.startswith('/welcome'):
			if self.user_id in self.adm_list:
				text = self.text.replace("/welcome ", "")
				with open('.tmp/welcome' + str(self.chat_id) + '.txt', 'w') as welcome:
					welcome.write(text)
				self.bot.sendMessage(
					self.chat_id,
					'As mensagens de boas-vindas foram alteradas com sucesso!'
				)
			else:
				self.bot.sendMessage(
					self.msg['chat']['id'],
					'Comando restrito aos administradores.'
				)

		if 'new_chat_member' in self.msg:
			user_first_name = str(self.msg['new_chat_member']['first_name'])
			get_bot_name = self.bot.getMe()
			bot_name = get_bot_name['first_name']

			if(user_first_name == bot_name):
				self.bot.sendMessage(self.chat_id, 'Olá, sou o Tycot!')
				sql.criar_table(self.chat_id)
			else:
				try:
					with open('.tmp/welcome' + str(self.chat_id) + '.txt', 'r') as welcome:
						welcome = welcome.read()
						welcome = welcome.replace('$name', user_first_name)
						self.bot.sendMessage(self.chat_id, welcome)
						sql.inserir(self.chat_id, self.msg['new_chat_member']['username'])
				except FileNotFoundError:
					print('Grupo sem um welcome' + str(self.chat_id) + '.txt')


	def keyboard(self):

		if self.text.startswith('/warn'):
			return InlineKeyboardMarkup(inline_keyboard=[
				[InlineKeyboardButton(text="Remove warn", callback_data='d')]
			])


	def add(self):

		if self.text.startswith('/addb'):
			sql.criar_table(self.chat_id)


		if sql.procurar(self.chat_id, self.msg['from']['id']) == 'erro ao procurar':
			sql.inserir(self.chat_id, self.msg['from']['id'])
		else:
			pass
