from telepot.namedtuple import InlineKeyboardButton, InlineKeyboardMarkup
from abc import ABCMeta, abstractmethod

class keyboard():
	def start_key(self):
		return InlineKeyboardMarkup(
			inline_keyboard=[
				[
					InlineKeyboardButton(
						text='Inicia uma conversa',
						url='https://telegram.me/TycotBot'
					)
				]
			]
		)

	def keyboard_warn(self, user_id):
			return InlineKeyboardMarkup(inline_keyboard=[
				[InlineKeyboardButton(text="Remove Warn", callback_data=str(user_id))]
			])
