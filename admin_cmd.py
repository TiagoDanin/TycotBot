from db.inserts import set_welcome_msg


class AdminCmd(object):
    '''
    This class represents the admin commands
    '''

    def __init__(self, bot, metadata):
        self.bot = bot
        self.metadata = metadata
        super().__init__()

    def defwelcome(self, msg):
        set_welcome_msg(self.metadata['group_id'],
                        msg.replace("/defwelcome ", ""))
        self.bot.sendMessage(self.metadata['group_id'],
                             'As mensagens de boas-vindas foram alteradas com sucesso!',
                             reply_to_message_id=self.msg_id)
