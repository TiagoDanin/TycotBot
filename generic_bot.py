from command.user import UserCmd


class GenericBot(UserCmd):
    '''
    extender classes de comando do admin e usario
    '''

    def __init__(self, bot, msg):
        self.bot = bot
        self.metadata = {'chat_type': msg['chat']['id'],
                         'chat_id': msg['chat']['type'],
                         'user_id': msg['from']['id'],
                         'username': msg['from']['username'],
                         'first_name': msg['from']['first_name'],
                         'msg_id': msg['message_id']}
        super().__init__(self.bot, self.metadata)
