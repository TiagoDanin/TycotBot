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
        output = ('<b>INFO</b>\n
                  '==================\n')
        chat_id = self.metadata['chat_id']
        if self.metadata['chat_type'] != 'private':
            # Get user warns
            user = get_user(self.metadata['user_id'])
            if user:
                user_adv = user[0].total_warns
            else:
                user_adv = 0

            max_warn = get_max_warns(self.metadata['chat_id'])

            output += (f'<pre>ID DO GRUPO</pre> : {chat_id}\n'
                       f'<pre>TOTAL DE ADVERTENCIAS</pre> : {max_warn}\n'
                       f'<pre>SUAS ADVERTENCIAS</pre> : {user_adv}\n')

        nome = self.metadata['username']
        id = self.metadata['user_id']
        output += (f'<pre>NOME</pre> : {nome}\n'
                   f'<pre>ID</pre>   : {id}')

        self.bot.sendMessage(
            chat_id=chat_id,
            parse_mode='HTML',
            text=output,
            reply_to_message_id=self.metadata['msg_id']
        )

    def help(self):
        help_msg = '''
Olá, sou o Tycot!
Segue abaixo minha lista de comandos:
/ajuda -> Mostra essa mensagem com lista de comandos.
/info -> Informações do grupo.
/link -> Link do grupo.
/regras -> Regras do grupo.
                   '''
        self.bot.sendMessage(self.metadata['user_id'], help_msg)

    @group.only
    def rules(self):
        rules = get_rules(self.metadata['chat_id'])
        if rules:
            self.bot.sendMessage(self.metadata['chat_id'], rules, parse_mode='HTML',
                                 reply_to_message_id=self.metadata['msg_id'])
        else:
            self.bot.sendMessage(self.metadata['chat_id'], '<b>Sem regras definidas no grupo!</b>',
                                 parse_mode='HTML',
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
