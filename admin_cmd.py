from db.inserts import set_welcome_msg, addto_db, commit_and_close, set_rules
from db.models.group import Group


class AdminCmd(object):
    '''
    This class represents the admin commands
    '''

    def __init__(self, bot, metadata):
        self.bot = bot
        self.metadata = metadata
        super().__init__()

    def start(self):
        '''
        Register the chat into the database
        '''
        addto_db(Group(self.metadata['chat_name'], self.metadata['chat_id']))
        commit_and_close()
        self.bot.sendMessage(self.metadata['chat_id'], 'Seu grupo foi cadastrado com sucesso!',
                             reply_to_message_id=self.metadata['msg_id'])

    def defwelcome(self, msg):
        set_welcome_msg(self.metadata['chat_id'],
                        msg.replace("/defwelcome ", ""))
        self.bot.sendMessage(self.metadata['chat_id'],
                             'A mensagem de boas-vindas foi alterada com sucesso!',
                             reply_to_message_id=self.metadata['msg_id'])

    def defrules(self, msg):
        set_rules(self.metadata['chat_id'],
                  msg.replace("/defregras ", ""))
        self.bot.sendMessage(self.metadata['chat_id'],
                             'As novas regras foram salvas com sucesso!',
                             reply_to_message_id=self.metadata['msg_id'])
