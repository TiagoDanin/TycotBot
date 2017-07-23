import telepot
import sys
from control_bot import control


TOKEN = sys.argv[1]
bot = telepot.Bot(TOKEN)

def handle(msg):
    control(msg, bot)


bot.message_loop(handle)

while 1: 
	pass
