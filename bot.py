import telepot
from control_bot import control


TOKEN = 'token'
bot = telepot.Bot(TOKEN)


def handle(msg):
    control(msg, bot)


bot.message_loop(handle)

while 1: 
	pass
