
class UserCmd:

    def __init__(self, bot, metadata):
        self.bot = bot
        self.metadata = metadata

    def info(self):
        if self.metadata['chat_type'] == 'private':
            self.bot.sendMessage(chat_id=self.metadata['chat_id'], parse_mode='Markdown',
                                 text=f'''*ID INFO*
                                 _*NOME*_:{self.metadata['user']}
                                 _*ID*_:{self.metadata['user_id']}''',
                                 reply_to_message_id=self.metadata['msg_id'])
