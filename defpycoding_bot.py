# -*- coding: UTF-8 -*-
#!/usr/bin/python3
import telebot, ast, re, requests
from buscar_modulo import buscar_modulo
from datetime import datetime
import sqlite3
from logs import log_msg, log_erros

token = ''
if not token:
    print("Esta faldando o token...")
    exit()

bot = telebot.TeleBot(token)
time = {}
def consulta_grupo(campo):
    db = sqlite3.connect('pycoding.db')
    db_cursor = db.cursor()
    resultado = db_cursor.execute('SELECT {campo} FROM grupo'
        .format(campo=campo)).fetchone()[0]
    db_cursor.close()
    return(resultado)

def block(mensagem):
    bot.reply_to(mensagem,'''
*Este bot esta programado para funcionar somente no grupo* [Python Coding - pt_BR](https://telegram.me/PyCoding)
''', parse_mode="Markdown")

def default(mensagem, comando, func):
    log_msg(mensagem)
    try:
        if mensagem.chat.id != -1001003662865 and  mensagem.from_user.id != 110806641:
            block(mensagem)
        else:
            bot.reply_to(mensagem, consulta_grupo(comando))
    except Exception as erro:
        log_erros(func, erro, mensagem)

def limite_comando(comando, atual):
    if time.get(comando):
        resultado = atual - time.get(comando)
        if resultado >= 10 or resultado <= -10:
            time[comando] = atual
            return(True)
        else:
            return(False)
    else:
        time[comando] = atual
        return(True)


########################################################################################################################
@bot.message_handler(commands=['adm', 'admin','admins', 'administradores', 'administrators', 'mod', 'moderadores', 'mods'])
def comando_adm(mensagem):
    if limite_comando('adm', datetime.today().minute) == True:
        default(mensagem, 'admins', 'comando ADM')
        
@bot.message_handler(commands=['ajuda', 'help'])
def comando_help(mensagem):
    if limite_comando('ajuda', datetime.today().minute) == True:
        default(mensagem, 'ajuda', 'comando HELP')

@bot.message_handler(commands=['regras', 'rules'])
def comando_regras(mensagem):
    if limite_comando('regras', datetime.today().minute) == True:
        default(mensagem, 'regras', 'comando REGRAS')

@bot.message_handler(commands=['link', 'link_convite', 'invite_link', 'add'])
def comando_link(mensagem):
    if limite_comando('link', datetime.today().minute) == True:
        default(mensagem, 'link', 'comando LINK')

@bot.message_handler(commands=['livros', 'book', 'books', 'apostilas', 'aprender_python'])
def comando_livros(mensagem):
    if limite_comando('aprender_python', datetime.today().minute) == True:
        default(mensagem, 'aprenderpython', 'comando APRENDER PYTHON')
        
@bot.message_handler(commands=['ide_python'])
def comando_ide(mensagem):
    if limite_comando('ide', datetime.today().minute) == True:
        default(mensagem, 'ide', 'comando IDE')

@bot.message_handler(commands=['sobre', 'about', 'contribuir'])
def comando_sobre(mensagem):
    if limite_comando('sobre', datetime.today().minute) == True:
        default(mensagem, 'sobre', 'comando SOBRE')

@bot.message_handler(commands=['sites'])
def comando_sobre(mensagem):
    if limite_comando('sites', datetime.today().minute) == True:
        default(mensagem, 'sites', 'comando SITES')

@bot.message_handler(commands=['sorteio'])
def comando_sobre(mensagem):
    if limite_comando('sorteio', datetime.today().minute) == True:
        default(mensagem, 'sorteio', 'comando SORTEIO')

@bot.message_handler(commands=['code'])
def comando_sugest(mensagem):
    log_msg(mensagem)
    if mensagem.chat.type != 'private':
        bot.reply_to(mensagem, '*Para usar esta função, me chame no PV*', parse_mode='Markdown')
    else:
        try:
            
            if len(mensagem.text) <= 6:
                bot.reply_to(mensagem, 'Código muito curto')
            else:
                bot.reply_to(mensagem, '```\n'+mensagem.text.replace('/code ', '')+'\n```', parse_mode="Markdown")
        except Exception as erro:
                log_erros('comando code', erro, mensagem)
                print('\n------------------------------------\nErro na função code, consulte o arquivo logs_de_erros,', datetime.today())

@bot.message_handler(func=lambda mensagem: True, content_types=['new_chat_participant'])
def comando_welcome(mensagem):
    default(mensagem, 'boas_vindas', 'comando WELCOME')

@bot.message_handler(commands=['ta_vivo?', 'TA_VIVO', 'Ta_Vivo', 'bot_on', 'status', 'bot_status', 'STATUS', 'bot'])
def id_(mensagem):
    log_msg(mensagem)
    if limite_comando('sorteio', datetime.today().minute) == True:
        try:
            bot.reply_to(mensagem,'''
            To Aqui ! o/
            Checando equipamentos...
            Sistema     [OK]
            Bateria     [OK]
            Munição     [OK]
            Explosivos  [OK]
            --------------------------
            Verificação completa !
            Data:       {hour}
            '''.format(hour = str(datetime.today())[:19]))
        except Exception as erro:
            log_erros('comando STATUS', erro, mensagem)
            print('\n------------------------------------\nErro na função status, consulte o arquivo logs_de_erros,', datetime.today())

@bot.message_handler(commands=['id'])
def id_(mensagem):
    log_msg(mensagem)
    try:
        bot.reply_to(mensagem,'''
INFO
ID: {id_user}
Seu Nome: {nome}
Username: @{username}
---------------------
Nome do Chat: {nome_grupo}
ID do Grupo:     {id_grupo}'''.format(nome = mensagem.from_user.first_name + mensagem.from_user.last_name if mensagem.from_user.last_name else mensagem.from_user.first_name,
                                    username = mensagem.from_user.username, id_user = mensagem.from_user.id, nome_grupo = mensagem.chat.title,
                                    id_grupo = mensagem.chat.id))
    except Exception as erro:
            log_erros('comando ID', erro, mensagem)
            print('\n------------------------------------\nErro na função ID, consulte o arquivo logs_de_erros,', datetime.today())

@bot.message_handler(commands=['buscar_modulo','buscar_modulos','busca_modulo'])
def comando_buscar_modulo(mensagem):
    log_msg(mensagem)
    if limite_comando('', datetime.today().minute) == True:
        if mensagem.chat.type != 'private':
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
    log_msg(mensagem)
    if mensagem.chat.id != -1001003662865 and  mensagem.from_user.id != 110806641:
            block(mensagem)
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
