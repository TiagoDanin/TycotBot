import telepot
import time
from datetime import datetime
from telepot.loop import MessageLoop

now = datetime.now()
bot = telepot.Bot('TOKEN')
updates = bot.getUpdates()
print(updates)

print("Bot inicializado!")


def welcome(msg):  # AJUSTAR AS BOAS-VINDAS
    content_type, chat_type, chat_id = telepot.glance(msg)
    text = msg['text']
    try:
        new_member = msg['new_chat_member']['first_name']
    except:
        new_member = 'Novo Membro'

    if(content_type == 'new_chat_member'):
        get_bot_name = bot.getMe()
        bot_name = get_bot_name['first_name']
        # bot_username = '@{}'.format(get_bot_name['username'])
        if(new_member == bot_name):
            bot.sendMessage(chat_id, 'Olá, sou o PygrameirosBot!')
        else:
            bot.sendMessage(chat_id, 'Seja bem vindo ao Pygrameiros, {}!'.format(new_member))

    if(text[0:8] == "/welcome"):
        user_id = msg['from']['id']
        admins = bot.getChatAdministrators(msg['chat']['id'])
        adm_list = [adm['user']['id'] for adm in admins]
        if (user_id in adm_list):
            text = text.replace("/welcome ", "")
            welcome = open('welcome.txt', 'w')
            welcome.write(text)
            welcome.close()
            bot.sendMessage(chat_id, "As novas mensagens de boas-vindas foram alteradas com sucesso!")


def rules(msg):
    text = msg['text']
    if(text[0:9] == "/setrules"):
        user_id = msg['from']['id']
        admins = bot.getChatAdministrators(msg['chat']['id'])
        adm_list = [adm['user']['id'] for adm in admins]
        if (user_id in adm_list):
            text = text.replace("/setrules ", "")
            rules = open('rules.txt', 'w')
            rules.write(text)
            rules.close()
            bot.sendMessage(msg['chat']['id'], "As novas regras foram salvas com sucesso!")

    if(text[0:7] == "/rules"):
            rules = open('rules.txt', 'r')
            rules = rules.read()
            bot.sendMessage(msg['chat']['id'], rules)


def log(msg):
    day = str(now.day)
    month = str(now.month)
    year = str(now.year)
    hour = str(now.hour)
    minute = str(now.minute)
    second = str(now.second)

    content_type, chat_type, chat_id = telepot.glance(msg)
    log = open('log.txt', 'a')
    users_register = open('users_register.txt', 'a')
    text = str(msg['text'])

    if(text == '/start' or text == '/start@PygrameirosBot'):
        users_register.write("log [{day}/{month}/{year}][{hour}:{minute}:{second}]"
                             .format(day=day, month=month, year=year,
                                     hour=hour, minute=minute, second=second))

        users_register.write(" | Username: {user} | ID: {id} | Comando usado: {comando}\n"
                             .format(user=msg['from']['username'], id=msg['from']['id'],
                                     comando=msg['text']))
        users_register.close()

        print("@{user} Iniciou o Bot - Dados salvos!".format(user=msg['from']['username']))

    else:
        log.write("log [{day}/{month}/{year}][{hour}:{minute}:{second}]"
                  .format(day=day, month=month, year=year,
                          hour=hour, minute=minute, second=second))

        log.write(" | Username: {user} | ID: {id} | Comando usado: {comando}\n"
                  .format(user=msg['from']['username'], id=msg['from']['id'], comando=msg['text']))

        log.close()
        print("@{user} Usou o Bot - Dados salvos!".format(user=msg['from']['username']))


def commands(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    text = msg['text']

    print(chat_type)
    print(chat_id)

    if(chat_type == 'private'):
        if(text == '/start' or text == '/start@PygrameirosBot'):
            bot.sendMessage(chat_id, ("Olá, eu sou o PygrameirosBot!"
                                      "\nFui criado pela galera do Pygrameiros para te ajudar"
                                      " a administrar teu grupo!"))
            # log(msg)

    if(text == '/info' or text == '/info@PygrameirosBot'):
        bot.sendMessage(chat_id, ("ID INFO \n\n NOME: {nome} "
                                  "\n ID: {id} \n NOME DO GRUPO: {nomeGrupo} "
                                  "\n ID GROUP: {idGrupo}").format(nome=msg['from']['username'],
                                                                   id=msg['from']['id'],
                                                                   nomeGrupo=msg['chat']['title'],
                                                                   idGrupo=chat_id))

    if(text == '/link' or text == '/link@PygrameirosBot'):
        bot.sendMessage(chat_id, 'Nosso link é: https://goo.gl/m0h2eQ')
        log(msg)

    if(text == '/help' or text == '/help@PygrameirosBot'):
        bot.sendMessage(chat_id, ('Olá, sou o PygrameirosBot!\nSegue a minha lista de comandos:\n'
                                  '/info -> Informações do grupo\n/link -> Link do grupo'))
        log(msg)
    ###  ADMINS COMMANDS  ###
    if(text == '/ban' or text == '/ban@PygrameirosBot'):
        user_id = msg['from']['id']
        user = msg['reply_to_message']['from']['first_name']
        reply_id = msg['reply_to_message']['from']['id']
        admins = bot.getChatAdministrators(chat_id)
        adm_list = [adm['user']['id'] for adm in admins]
        if (user_id in adm_list):
            if reply_id not in adm_list:
                bot.sendMessage(chat_id, "*{}* foi banido".format(user), parse_mode="Markdown")
                bot.kickChatMember(chat_id, reply_id)
            else:
                bot.sendMessage(chat_id, '*{}* é adm do grupo'.format(user), "Markdown")
        else:
            bot.sendMessage(chat_id, 'Apenas administradores podem usar este comando.')

        if(text == '/kick' or text == '/kick@PygrameirosBot'):
            user_id = msg['from']['id']
            user = msg['reply_to_message']['from']['first_name']
            reply_id = msg['reply_to_message']['from']['id']
            admins = bot.getChatAdministrators(chat_id)
            adm_list = [adm['user']['id'] for adm in admins]
            if (user_id in adm_list):
                if reply_id not in adm_list:
                    bot.sendMessage(chat_id, "*{}* foi retirado do grupo.".format(user),
                                    parse_mode="Markdown")
                    bot.kickChatMember(chat_id, reply_id)
                else:
                    bot.sendMessage(chat_id, '*{}* é adm do grupo'.format(user), "Markdown")
            else:
                bot.sendMessage(chat_id, 'Apenas administradores podem usar este comando.')


def handle(msg):
    log(msg)
    commands(msg)
    welcome(msg)
    rules(msg)


MessageLoop(bot, handle).run_as_thread()
while 1:
    time.sleep(10)
