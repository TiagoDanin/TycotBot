import telepot
import sys
from control_bot import control


# TOKEN = "sys.argv[1]"
TOKEN = "403341313:AAFTK0PYmwSk7wG5g-8xdVrzuoOPZzsOC9s"
bot = telepot.Bot(TOKEN)

def handle(msg):
    use_bot = control(msg, bot)

    use_bot.log()
    use_bot.commands()
    use_bot.goodbye()
    use_bot.rules()
    use_bot.welcome()
    use_bot.add()

bot.message_loop(handle)

while 1:
	pass
