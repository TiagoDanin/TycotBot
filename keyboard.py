from telepot.namedtuple import InlineKeyboardButton, InlineKeyboardMarkup
from abc import ABCMeta, abstractmethod


class keyboard():
	def start_key(self):
		return InlineKeyboardMarkup(
			inline_keyboard=[
				[
					InlineKeyboardButton(
						text='Inicia uma conversa',
						url='https://t.me/TycotBot?start=start'
					)
				]
			]
		)
	def keyboard_alert(self, chat_id, msg, usuario):
		return InlineKeyboardMarkup(inline_keyboard=[
			[InlineKeyboardButton(text="Ver mensagem", callback_data='alerta '+ str(chat_id)+' '+str(msg)+' '+str(usuario))]
			])

	def keyboard_warn(self, user_id):
			return InlineKeyboardMarkup(inline_keyboard=[
				[InlineKeyboardButton(text="Remove Warn", callback_data='unwarn '+ str(user_id))]
			])

	def keyboard_sugestao(self):
			return InlineKeyboardMarkup(inline_keyboard=[
				[InlineKeyboardButton(text="Sugestão de Leitura", callback_data='sugestao ')]
			])