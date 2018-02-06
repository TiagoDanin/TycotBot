from db.queries import get_rules, get_link, get_max_warns


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
            msg = ('<b>ID INFO</b>\n'
                   '==================\n'
                   '<code>ID DO GRUPO</code> : {chat_id}\n'
                   '<code>TOTAL DE ADVERTENCIAS</code> : {max_warn}\n'
                   '<code>NOME</code> : {nome}\n'
                   '<code>ID</code>   : {id}')
            self.bot.sendMessage(chat_id=self.metadata['chat_id'], parse_mode='html',
                                 text=msg.format(chat_id=self.metadata['chat_id'],
                                                 max_warn=get_max_warns(self.metadata['chat_id']),
                                                 nome=self.metadata['username'],
                                                 id=self.metadata['user_id']),
                                 reply_to_message_id=self.metadata['msg_id'])
        else:
            msg = ('<b>ID INFO</b>\n'
                   '==================\n'
                   '<code>NOME</code> : {nome}\n'
                   '<code>ID</code>   : {id}') 
            self.bot.sendMessage(chat_id=self.metadata['chat_id'], parse_mode='html',
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

    def rules(self):
        rules = get_rules(self.metadata['chat_id'])
        if rules:
            self.bot.sendMessage(self.metadata['chat_id'], rules, parse_mode='Markdown',
                                 reply_to_message_id=self.metadata['msg_id'])
        else:
            self.bot.sendMessage(self.metadata['chat_id'], '*Sem regras!*', parse_mode='Markdown')

    def link(self):
        if self.metadata['chat_type'] == 'supergroup':
            link = self.bot.exportChatInviteLink(self.metadata['chat_id'])
            self.bot.sendMessage(self.metadata['chat_id'], link,
                                 reply_to_message_id=self.metadata['msg_id'])
        else:
            link = get_link(self.metadata['chat_id'])
            self.bot.sendMessage(self.metadata['chat_id'], link,
                                 reply_to_message_id=self.metadata['msg_id'])
