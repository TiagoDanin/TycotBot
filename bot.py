import telepot
from telepot.loop import MessageLoop
import sys
from control_bot import control
from bot_command import *
from time import time, sleep
from datetime import date
from keyboard import keyboard
import schedule

TOKEN = sys.argv[1]
bot = telepot.Bot(TOKEN)

def msgDia():
	inst_keyboard = keyboard()
	msg = ['Coders', 'Jedi\'s', 'Programeiros']
	hj = date.today().weekday()
	#podem mudar as frases. Não sou tão criativo. ^^
	if hj == 0:
		hoje = ' Força que hoje é só o primeiro dia da semana!'
	elif hj == 2:
		hoje = ' Estamos no meio da semana. Tycot deseja-lhes muita sabedoria e paciência'
	elif hj == 4:
		hoje = ' Hoje é sexta! Não façam besteira ou vão perder o FDS!'
		#infelizmente, como está fora do handle, não há como pegar o ID do grupo. Se alguém souber, fique a vontade.
	bot.sendMessage(-1001068576090, parse_mode='HTML', 
		text='<i>Bom dia {}!{}</i>'.format(msg[random.randint(0,len(msg)-1)], hoje), reply_markup = inst_keyboard.keyboard_sugestao()) 
	bot.sendVideo(-1001068576090,
		'https://media.giphy.com/media/W4IY7zQdRh7Ow/giphy.gif')

def handle(msg):
	main = control(msg, bot)
	inst_command_user = command_user(msg=msg, bot=bot)
	inst_command_admin = command_admin(msg=msg, bot=bot)

	if msg.get('data'):
		msgDataSplit = msg['data'].split()
		if msgDataSplit[0] == 'unwarn':
				text = 'None'
				ctext = 'None'
				inst_command_admin.unwarn(data=msgDataSplit[1])
		elif msgDataSplit[0] == 'alerta':
			inst_command_user.enviarAlerta(chat_id=msgDataSplit[1], data=msgDataSplit[2], usuario=msgDataSplit[3])
		elif msgDataSplit[0] == 'sugestao':
			inst_command_user.verify_book()	
		else:
			pass
		
	else:
		try:
			if(msg['reply_to_message'] != None):
				user_id = msg['reply_to_message']['from']['id']
				inst_command_user.buscarAlerta(user_id=user_id)
		except:
				pass
		try:
			msgEntidade = msg['entities']
			msgArray = msgEntidade[0]
			if(msgArray['type'] == 'text_mention'):
				user_id = msgArray['user']['id']
				inst_command_user.buscarAlerta(user_id=user_id)

			text = msg['text'].split(' ')
			ctext = text[0].lower()
		except BaseException:
			text = None
			ctext = None

		admin_commands = {
			'/ban': inst_command_admin.ban,
			'/warn': inst_command_admin.warn,
			'/unwarn': inst_command_admin.unwarn,
			'/deflink': inst_command_admin.deflink,
			'/defregras': inst_command_admin.defregras,
			'/welcome': inst_command_admin.defwelcome,
			'/addb': inst_command_admin.add
		}

		user_command = {
			'/start': inst_command_user.start,
			'/info': inst_command_user.info,
			'/ajuda': inst_command_user.ajuda,
			'/link': inst_command_user.link,
			'/regras': inst_command_user.regras,
			'/verifybook': inst_command_user.verify_book,
			'/alertoff': inst_command_user.remAlerta,
			'/alert': inst_command_user.aceitarAlerta,
		}

		others = {
			'left_chat_member': inst_command_user.goodbye,
			'new_chat_member': inst_command_user.new_member
		}

		if msg.get('left_chat_member'):
			others['left_chat_member']()
		elif msg.get('new_chat_member'):
			others['new_chat_member']()

		if admin_commands.get(ctext):
			if ctext.startswith('/deflink'):
				admin_commands[ctext](msg['text'])
			elif ctext.startswith('/defregras'):
				admin_commands[ctext](msg['text'])
			elif ctext.startswith('/welcome'):
				admin_commands[ctext](msg['text'])
			else:
				admin_commands[ctext]()

		elif user_command.get(ctext):
			user_command[ctext]()

if __name__ == '__main__':
	MessageLoop(bot, handle).run_as_thread()
	schedule.every().monday.at('07:00').do(msgDia)
	schedule.every().wednesday.at('07:00').do(msgDia)
	schedule.every().friday.at('07:00').do(msgDia)
while True:
	schedule.run_pending()
	sleep(100)
