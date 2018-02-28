from decorators import group
from db.queries import get_rules, get_link, get_max_warns, get_user


class UserCmd(object):
    '''
    This class represents the user commands
    '''

    def __init__(self, bot, metadata):
        self.bot = bot
        self.metadata = metadata
        super().__init__()

    def info(self):
        '''
        Show information about the user or group
        '''
        if self.metadata['chat_type'] != 'private':
            msg = ('*INFO*\n'
                   '==================\n'
                   '`ID DO GRUPO` : {chat_id}\n'
                   '`TOTAL DE ADVERTENCIAS` : {max_warn}\n'
                   '`SUAS ADVERTENCIAS` : {user_adv}\n'
                   '`NOME` : {nome}\n'
                   '`ID`   : {id}')
            # get user warns
            user = get_user(self.metadata['user_id'])
            if user:
                user_adv = user[0].total_warns
            else:
                user_adv = 0

            self.bot.sendMessage(chat_id=self.metadata['chat_id'], parse_mode='Markdown',
                                 text=msg.format(chat_id=self.metadata['chat_id'],
                                                 max_warn=get_max_warns(self.metadata['chat_id']),
                                                 user_adv=user_adv,
                                                 nome=self.metadata['username'],
                                                 id=self.metadata['user_id']),
                                 reply_to_message_id=self.metadata['msg_id'])
        else:
            msg = ('*ID INFO*\n'
                   '==================\n'
                   '`NOME` : {nome}\n'
                   '`ID`   : {id}')
            self.bot.sendMessage(chat_id=self.metadata['chat_id'], parse_mode='Markdown',
                                 text=msg.format(nome=self.metadata['username'],
                                                 id=self.metadata['user_id']),
                                 reply_to_message_id=self.metadata['msg_id'])

    def help(self):
        help_msg = '''
Olá, sou o Tycot!
Segue minha lista de comandos:
    /ajuda -> mostra essa mensagem
    /info -> informações do grupo
    /link -> link do grupo
    /regras -> regras do grupo
    /verifybook -> verifica o ultimo livro do packtpub
                          '''
        self.bot.sendMessage(self.metadata['user_id'], help_msg)

    @group.only
    def rules(self):
        rules = get_rules(self.metadata['chat_id'])
        if rules:
            self.bot.sendMessage(self.metadata['chat_id'], rules, parse_mode='Markdown',
                                 reply_to_message_id=self.metadata['msg_id'])
        else:
            self.bot.sendMessage(self.metadata['chat_id'], '*Sem regras definidas no grupo!*',
                                 parse_mode='Markdown',
                                 reply_to_message_id=self.metadata['msg_id'])

    @group.only
    def link(self):
        if self.metadata['chat_type'] == 'supergroup':
            link = self.bot.exportChatInviteLink(self.metadata['chat_id'])
            self.bot.sendMessage(self.metadata['chat_id'], link,
                                 reply_to_message_id=self.metadata['msg_id'])
        else:
            link = get_link(self.metadata['chat_id'])
            self.bot.sendMessage(self.metadata['chat_id'], link,
                                 reply_to_message_id=self.metadata['msg_id'])
