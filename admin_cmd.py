from db.inserts import (set_welcome_msg, addto_db, commit_and_close, set_rules, set_chat_link,
                        warn_user, set_max_warn, unwarn_user, add_user)
from db.queries import get_max_warns, get_user, chat_exist
from db.models.group import Group


class AdminCmd(object):
    '''
    This class represents the admin commands
    '''

    def __init__(self, bot, metadata, tycot):
        self.bot = bot
        self.metadata = metadata
        self.tycot = tycot
        super().__init__()

    def start(self):
        '''
        Register the chat into the database
        '''
        if not chat_exist(self.metadata['chat_id']):
            addto_db(Group(self.metadata['chat_name'], self.metadata['chat_id']))
            commit_and_close()
            self.bot.sendMessage(self.metadata['chat_id'], 'Seu grupo foi cadastrado com sucesso!',
                                 reply_to_message_id=self.metadata['msg_id'])
        else:
            self.bot.sendMessage(self.metadata['chat_id'], '*Seu grupo já está cadastrado!*',
                                 parse_mode='Markdown',
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
        user_first_name = self.metadata['rpl_first_name']
        user_id = self.metadata['rpl_user_id']
        msg_id = self.metadata['rpl_msg_id']
        self.bot.kickChatMember(self.metadata['chat_id'], user_id)
        self.bot.sendMessage(self.metadata['chat_id'],
                             f'<b>{user_first_name}</b> foi retirado do grupo.', parse_mode='HTML',
                             reply_to_message_id=msg_id)

    def deflink(self, msg):
        ''' See: https://core.telegram.org/bots/api#exportchatinvitelink'''
        if self.metadata['chat_type'] == 'supergroup':
            self.bot.sendMessage(self.metadata['chat_id'],
                                 'Link já foi definido por padrão.',
                                 reply_to_message_id=self.metadata['msg_id'])
        else:
            set_chat_link(self.metadata['chat_id'],
                          msg.replace("/deflink ", ""))
            self.bot.sendMessage(self.metadata['chat_id'],
                                 'Link do grupo salvo com sucesso!',
                                 reply_to_message_id=self.metadata['msg_id'])

    def maxwarn(self, msg):
        set_max_warn(self.metadata['chat_id'],
                     msg.replace("/defmaxwarn ", ""))
        self.bot.sendMessage(self.metadata['chat_id'],
                             'Total de advertencias salvas com sucesso!',
                             reply_to_message_id=self.metadata['msg_id'])

    def _kick_user(self, user_id):
        group_max_warn = get_max_warns(self.metadata['chat_id'])
        user_name = self.metadata['rpl_first_name']
        user = get_user(user_id)
        if user.total_warns >= group_max_warn:
            self.bot.sendMessage(self.metadata['chat_id'],
                                 f'*{user_name}* expulso por atingir o\
                                 limite de advertencias.',
                                 parse_mode='Markdown',
                                 reply_to_message_id=self.metadata['rpl_msg_id'])
            self.bot.kickChatMember(self.metadata['chat_id'], self.metadata['rpl_user_id'])

    def warn(self):
        first_name = self.metadata['rpl_first_name']
        user_id = self.metadata['rpl_user_id']
        msg_id = self.metadata['rpl_msg_id']
        if user_id in self.tycot.is_adm():
            self.bot.sendMessage(self.metadata['chat_id'],
                                 f'*{first_name}* é um dos administradores.\
                                 Não posso advertir administradores.', parse_mode='Markdown',
                                 reply_to_message_id=self.metadata['msg_id'])
        else:
            user = add_user(first_name, user_id)
            group_max_warns = get_max_warns(self.metadata['chat_id'])
            warn_user(self.metadata['chat_id'], user_id)
            self.bot.sendMessage(self.metadata['chat_id'],
                                 f'{first_name} *foi advertido* \
                                 ({user.total_warns}/{group_max_warns}).',
                                 parse_mode='Markdown',
                                 reply_markup=self.keyboard_warn(user_id),
                                 reply_to_message_id=msg_id)
            self._kick_user(user_id)

    def unwarn(self):
        user_id = self.metadata['rpl_user_id']
        if user_id in self.tycot.is_adm():
            self.bot.sendMessage(self.metadata['chat_id'],
                                 'Administradores não possuem advertências.',
                                 reply_to_message_id=self.metadata['msg_id'])
        else:
            unwarn_user(self.metadata['chat_id'], user_id)
