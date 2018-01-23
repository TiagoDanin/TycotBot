from command.user import UserCmd
from command.admin import AdminCmd


class TycotBot(object):

    def __init__(self, bot, msg):
        self.bot = bot
        self.metadata = {'chat_id': msg['chat']['id'],
                         'chat_type': msg['chat']['type'],
                         'user_id': msg['from']['id'],
                         'username': msg['from']['username'],
                         'first_name': msg['from']['first_name'],
                         'msg_id': msg['message_id']}

        self.usercmd = UserCmd(self.bot, self.metadata)
        self.admcmd = AdminCmd(self.bot, self.metadata)
