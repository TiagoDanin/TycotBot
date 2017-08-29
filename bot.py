import telepot
from telepot.loop import MessageLoop
import sys
from control_bot import control
from bot_command import *
from time import sleep
import re

TOKEN = sys.argv[1]
bot = telepot.Bot(TOKEN)

def handle(msg):
	main = control(msg, bot)
	inst_command_user = command_user(msg=msg, bot=bot)
	inst_command_admin = command_admin(msg=msg, bot=bot)

	if msg.get('data'):
		text = 'None'
		ctext = 'None'
		inst_command_admin.unwarn(data=msg['data'])
	else:
		try:
			if 'text' in msg:
				frase = msg['text']
				result = re.search('(?<=@)\w+', frase)
				if(result is not None):
					usuario = result.group(0)
					inst_command_user.buscarAlerta(usuario=usuario)

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

		if msg.get('left_chat_member'):
			others['left_chat_member']()
		elif msg.get('new_chat_member'):
			others['new_chat_member']()

if __name__ == '__main__':
	MessageLoop(bot, handle).run_as_thread()

while True:
	sleep(100)
