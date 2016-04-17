# -*- coding: UTF-8 -*-
#!/usr/bin/python3
import telebot, ast, re, requests
from buscar_modulo import buscar_modulo
from datetime import datetime
import sqlite3
from logs import log_msg, log_erros

token = ''
if token == '':
    print("Esta faldando o token...")
    quit()
bot = telebot.TeleBot(token)

def consulta_grupo(campo):
    db = sqlite3.connect('pycoding.db')
    db_cursor = db.cursor()
    return(db_cursor.execute('SELECT {campo} FROM grupo'
                             .format(campo=campo)).fetchone()[0])
def block(mensagem):
    bot.reply_to(mensagem,'''
*Este bot esta programado para funcionar somente no grupo* [Python Coding - BS|EH](https://telegram.me/PyCoding)
''', parse_mode="Markdown")

def default(mensagem, comando, func):
    log_msg(mensagem)
    try:
        if mensagem.chat.id != -1001003662865:
            block(mensagem)
        else:
            bot.reply_to(mensagem, consulta_grupo(comando))
    except Exception as erro:
        log_erros(func, erro, mensagem)

########################################################################################################################

@bot.message_handler(commands=['adm', 'admin','admins', 'administradores', 'administrators', 'mod', 'moderadores', 'mods'])
def comando_adm(mensagem):
    default(mensagem, 'admins', 'comando ADM')

@bot.message_handler(commands=['ajuda', 'help'])
def comando_help(mensagem):
    default(mensagem, 'ajuda', 'comando HELP')

@bot.message_handler(commands=['regras', 'rules'])
def comando_regras(mensagem):
    default(mensagem, 'regras', 'comando REGRAS')

@bot.message_handler(commands=['link', 'link_convite', 'invite_link', 'add'])
def comando_link(mensagem):
    default(mensagem, 'link', 'comando LINK')

@bot.message_handler(commands=['livros', 'book', 'books', 'apostilas'])
def comando_livros(mensagem):
    default(mensagem, 'livros', 'comando LIVROS')

@bot.message_handler(commands=['ide_python'])
def comando_ide(mensagem):
    default(mensagem, 'ide', 'comando IDE')

@bot.message_handler(commands=['sobre', 'about', 'contribuir'])
def comando_sobre(mensagem):
    default(mensagem, 'sobre', 'comando SOBRE')

@bot.message_handler(commands=['sites'])
def comando_sobre(mensagem):
    default(mensagem, 'sites', 'comando SITES')

@bot.message_handler(func=lambda mensagem: True, content_types=['new_chat_participant'])
def comando_welcome(mensagem):
    default(mensagem, 'boas_vindas', 'comando WELCOME')

@bot.message_handler(commands=['id'])
def id_(mensagem):
    log_msg(mensagem)
    try:
        bot.reply_to(mensagem,'''
*INFO*
ID: `{id_user}`
Seu Nome: {nome}
Username: @{username}
---------------------
Nome do Chat: {nome_grupo}
ID do Grupo:     `{id_grupo}`'''.format(nome = mensagem.from_user.first_name + mensagem.from_user.last_name if mensagem.from_user.last_name else mensagem.from_user.first_name,
                                    username = mensagem.from_user.username, id_user = mensagem.from_user.id, nome_grupo = mensagem.chat.title,
                                    id_grupo = mensagem.chat.id), parse_mode='Markdown')
    except Exception as erro:
            log_erros('comando ID', erro, mensagem)
            print('\n------------------------------------\nErro na função ID, consulte o arquivo logs_de_erros,', datetime.today())

@bot.message_handler(commands=['buscar_modulo','buscar_modulos','busca_modulo'])
def comando_buscar_modulo(mensagem):
    log_msg(mensagem)
    if (str(mensagem.chat.type) != 'private'):
        bot.reply_to(mensagem, '*Para usar esta função, me chame no PV*', parse_mode='Markdown')
    else:
        try:
            texto = mensagem.text.split(' ')[1]
            if len(texto) > 2:
                resposta = buscar_modulo(texto)
                if resposta:
                    resposta = ''.join(x for x in resposta)
                    resposta = telebot.util.split_string(resposta, 3000)
                    for x in resposta: bot.reply_to(mensagem,x)
                else:
                    bot.reply_to(mensagem,'_Nenhum módulo encontrado_', parse_mode='Markdown')
            else:
                bot.reply_to(mensagem,'_Termo de busca muito curto, tente novamente_', parse_mode='Markdown')
        except IndexError:
            bot.reply_to(mensagem,'Uso: `/buscar_modulo <termo de busca>`\n_Ex.: /buscar_[_]()_modulo telegram_', parse_mode='Markdown')
        except Exception as erro:
            log_erros('comando buscar_modulo', erro, mensagem)
            print('\n------------------------------------\nErro na função buscar_modulo, consulte o arquivo logs_de_erros,', datetime.today())

@bot.message_handler(commands=['sugestão', 'sugestao'])
def comando_sugest(message):
    log(message)
    if (str(message.chat.type) != 'private') and (str(message.chat.id) not in str(grupos_liberados)):
        block(message)
    else:
        if len(message.text) > 10:
            arq_sugest = open('sugest.txt', 'a')
            arq_sugest.write('\n\n'+'-'*30+'\n'+message.text.replace('/sugestão ', ''))
            arq_sugest.close()
            bot.reply_to(message,'*Sugestão recebida, obrigado*', parse_mode='Markdown')
        else:
            bot.reply_to(message,'Uso: `/sugestão <sugestão>`', parse_mode='Markdown')

print('Bot Iniciado')
bot.polling()
