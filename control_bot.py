import telepot
import logging
import sql
from datetime import datetime
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton


class control:

	day_date_hour = datetime.now().strftime('%c')

	def __init__(self, msg, bot):
		
		self.bot = bot
		if msg.get('data'):
			self.query_id, self.from_id, self.query_data = telepot.glance(msg, flavor='callback_query')
			self.chat_id = msg['message']['chat']['id']
			self.chat_type = msg['message']['chat']['type']
			self.UserID = msg['from']['id']
			self.msg = msg
		else:
			self.content_type, self.chat_type, self.chat_id = telepot.glance(msg)
			self.msg_id = msg['message_id']
			
			self.user = msg['from']['first_name']
			self.username = msg['from']['username']
			self.UserID = msg['from']['id']
			self.msg = msg


	def get_admin_list(self, query=False, user_reply=False):
		admin = self.bot.getChatAdministrators(self.chat_id)
		AdminID_list = [adminID['user']['id'] for adminID in admin]

		if user_reply:
			return AdminID_list
		
		elif query:
			if self.UserID in AdminID_list:
				return True
			else:
				self.bot.answerCallbackQuery(callback_query_id=self.query_id, 
											text='Você não esta permitido a usar esse botão!',
											show_alert=False,
											cache_time=1)
			return False

		elif self.UserID in AdminID_list:
				return True

		self.bot.sendMessage(chat_id=self.chat_id,
							 parse_mode='HTML', 
							 text='<b>Apenas administradores podem usar este comando.</b>')



