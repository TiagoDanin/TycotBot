
def only(func):
    def inner(*args, **kwargs):
        if args[0].metadata['chat_type'] == 'private':
            args[0].bot.sendMessage(args[0].metadata['chat_id'],
                                    '*Este comando só funciona em grupos!*', parse_mode='Markdown',
                                    reply_to_message_id=args[0].metadata['msg_id'])
            return
        func(*args, **kwargs)
    return inner
