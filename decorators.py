import logging
from datetime import datetime

def decor_info_ajuda(func):
	def wrapper(*args, **kwargs):
		try:
			func(*args,**kwargs)
		except:
			args[0].bot.sendMessage(
				 args[0].chat_id,
				'Por favor, inicie uma conversa comigo e tente novamente.'
			)
	return wrapper

def log(func):
	day_date_hour = datetime.now().strftime('%c')

	def wrapper(*args,**kwargs):
		if args[0].msg.get('data'):
			func(*args, **kwargs)
		else:
			func(*args, **kwargs)
			if args[0].msg['text'].startswith('/start'):
				logging.basicConfig(filename='.tmp/users_register.log', filemode='w', level=logging.INFO)
				logging.info("log [{}]".format(day_date_hour))
				logging.info(" | Username: {} | ID: {} | Comando usado: {}\n".format(
				args[0].user,
				args[0].UserID, 
				args[0].msg['text'].split(' ')[0]))
				print("@{} Iniciou o Bot - Dados salvos!".format(args[0].user))
			elif(args[0].msg['text'].startswith('/') and args[0].msg['text'] != '/start'):
				logging.basicConfig(filename='.tmp/log.log', filemode='w', level=logging.INFO)
				logging.info("log [{}]".format(day_date_hour))
				logging.info(" | Username: {} | ID: {} | Comando usado: {}\n".format(
				args[0].user,
				args[0].UserID, 
				args[0].msg['text'].split(' ')[0]))
				print("@{} Usou o Bot - Dados salvos!".format(args[0].user))
	return wrapper


def admin(func):
	def wrapper(*args, **kwargs):
		if args[0].msg.get('data'):
			if args[0].get_admin_list(query=True):
				func(*args,**kwargs)
		elif args[0].get_admin_list():
			func(*args,**kwargs)
	return wrapper