from db.inserts import set_welcome_msg, addto_db, commit_and_close, set_rules, set_chat_link
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

    def ban(self, msg):
        user_first_name = msg['reply_to_message']['from']['first_name']
        user_id = msg['reply_to_message']['from']['id']
        msg_id = msg['reply_to_message']['message_id']
        self.bot.kickChatMember(self.metadata['chat_id'], user_id)
        self.bot.sendMessage(self.metadata['chat_id'],
                             f'<b>{user_first_name}</b> foi retirado do grupo.', parse_mode='HTML',
                             reply_to_message_id=msg_id)

    def deflink(self, msg):
        set_chat_link(self.metadata['chat_id'],
                      msg.replace("/deflink ", ""))
        self.bot.sendMessage(self.metadata['chat_id'],
                             'Link do grupo salvo com sucesso!',
                             reply_to_message_id=self.metadata['msg_id'])
