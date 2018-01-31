from user_cmd import UserCmd
from admin_cmd import AdminCmd
from db.inserts import create_tables
from db.queries import get_welcome_msg


class TycotBot(object):

    def __init__(self, bot, msg):
        create_tables()
        self.bot = bot
        self.metadata = {'chat_id': str(msg['chat']['id']),
                         'chat_type': msg['chat']['type'],
                         'user_id': str(msg['from']['id']),
                         'username': msg['from']['username'],
                         'first_name': msg['from']['first_name'],
                         'msg_id': msg['message_id']}
        if self.metadata['chat_type'] != 'private':
            self.metadata['chat_name'] = msg['chat']['title']

        self.usercmd = UserCmd(self.bot, self.metadata)
        self.admcmd = AdminCmd(self.bot, self.metadata)

    def events(self, msg):
        '''
        Verify if a new member joined the group or left
        '''
        if 'new_chat_member' in msg:
            self.new_member(msg)
        elif 'left_chat_member' in msg:
            self.left_member(msg)

    def new_member(self, msg):
        '''
        Send a mensage when a new member joined the group
        '''
        user_first_name = msg['new_chat_member']['first_name']

        welcome = get_welcome_msg(self.metadata['chat_id'])
        welcome = welcome.replace('$user', user_first_name)
        self.bot.sendMessage(self.metadata['chat_id'], welcome, parse_mode='Markdown')

    def left_member(self, msg):
        '''
        Send a mensage when a new member left the group
        '''
        user_first_name = msg['left_chat_member']['first_name']
        self.bot.sendMessage(self.metadata['chat_id'], "Tchau, {}".format(user_first_name))
        self.bot.sendVideo(self.metadata['chat_id'],
                           'https://media.giphy.com/media/l3V0gpbjA6fD7ym9W/giphy.mp4')
