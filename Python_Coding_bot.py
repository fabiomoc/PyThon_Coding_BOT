# -*- coding: UTF-8 -*-
import telebot, ast
from buscar_modulo import buscar_modulo
from datetime import datetime


token = '<BOT TOKEN>'
bot = telebot.TeleBot(token)

grupos_liberados = [<grupos liberados>]
def log_erros(func, erro,mensagem):
    arq = open('Logs_de_erros.txt', 'a')
    data = str()
    arq.write('''

#Erro! Função {fun} {data}
Mensagem de erro:
{log_erro}
Mensagem que originou o erro:
{mensagem}
------------------------------------'''
                  .format(fun = func, data = str(datetime.today()), log_erro = erro, mensagem = str(mensagem).encode('UTF-8', errors='ignore').decode('ASCII', errors='ignore')))
        
    arq.close()

def log(dados_msg):
    try:
        dados_msg = ast.literal_eval(str(dados_msg).encode('UTF-8', errors='ignore').decode('ASCII', errors='ignore'))
        if dados_msg['chat']['type'] == 'private': origem = 'Mensagem Privada'
        elif dados_msg['chat']['type'] == 'group': origem = 'Grupo'
        elif dados_msg['chat']['type'] == 'supergroup': origem = 'Super Grupo'
        else: origem = dados_msg['chat']['type']
        print('''

LOG: comando recebido
Comando: {comando}
Origem: {origem}
Titulo do chat: {nomechat}
ID do chat: {chatid}
Nome do remetente: {nome_usuario}
Username: {username}'''
              .format(comando = dados_msg['text'], origem = origem, nomechat = dados_msg['chat']['title'], chatid = dados_msg['chat']['id'],
                        nome_usuario = dados_msg['from_user']['first_name'] + dados_msg['from_user']['last_name'] if dados_msg['from_user']['last_name'] else dados_msg['from_user']['first_name'],
                          username = dados_msg['from_user']['username']))
    except Exception as erro:
        log_erros('LOG', erro, dados_msg)
        print('Erro na função log, consulte o arquivo logs_de_erros,', datetime.today())
        
def block(mensagem):
    bot.reply_to(mensagem,'''
Este bot esta programado para funcionar somente no grupo Python Coding - BS|EH
Entre para o grupo usando este link: https://telegram.me/joinchat/BprGcTvSrhHJIFlsjlLc5Q

Para conseguir autorização para este chat, entre em contato com meu desenvolvedor, @EXPL01T3R0''')


@bot.message_handler(commands=['buscar_modulo','buscar_modulos','busca_modulo'])
def comando_buscar_modulo(message):
    log(message)
    if (str(message.chat.type) != 'private') and (str(message.chat.id) not in str(grupos_liberados)):
        block(message)
    else:
        try:
            texto = message.text.split(' ')[1]
            if len(texto) > 2:
                resposta = buscar_modulo(texto)
                if resposta:
                    resposta = ''.join(x for x in resposta)
                    resposta = telebot.util.split_string(resposta, 3000)
                    for x in resposta: bot.reply_to(message,x)
                else:
                    bot.reply_to(message,'Nenhum módulo encontrado')
            else:
                bot.reply_to(message,'termo de busca muito curto, tente novamente')
        except IndexError:
            bot.reply_to(message,'uso: /buscar_modulo <termo de busca> (ex.: /buscar_modulo telegram)')
        except Exception as erro:
            log_erros('buscar_modulo', erro, dados_msg)
            print('Erro na função buscar_modulo, consulte o arquivo logs_de_erros,', datetime.today())

@bot.message_handler(commands=['sobre', 'about', 'contribuir'])
def comando_sobre(message):
    log(message)
    bot.reply_to(message,'''
PyCoding BOT v.1.0
Bot Oficial do grupo Python Coding - BS|EH

Desenvolvido por @EXPL01T3R0

Contribua ;) : https://github.com/diego-bernardes/PyThon_Coding_BOT
''')


@bot.message_handler(commands=['ajuda', 'help'])
def comando_help(message):
    log(message)
    bot.reply_to(message,'''
/buscar_modulo <termo de busca> Realiza uma busca por modulos python (ex.: /buscar_modulos telegram)

/ide_python Retorna links de IDEs python, gratuitas e proprietárias

livros Retorna o link da biblioteca de livros e apostilas sobre python do grupo

/link Retorna o Link de convite para acesso ao grupo

/help Retorna a lista de comandos ativos

/regras Exibe as regras vigentes no grupo

/Sobre | /about | /contribuir Exibe informações sobre o bot e como contruir com o mesmo

/sugestão | /sugestao <texto> Envie sugestões de melhorias para o bot

''')
        

@bot.message_handler(commands=['regras', 'rules'])
def comando_regras(message):
    log(message)
    if (str(message.chat.type) != 'private') and (str(message.chat.id) not in str(grupos_liberados)):
        block(message)
    else:
        bot.reply_to(message,'''
[*] Grupo criado de discussão sobre Python e tecnologia de uma maneira geral

REGRAS
======================
[X] Flood:
Punição: BAN

[X] Adicionar bots s/ permissão:
Punição: 1° ocorrência, AVISO
Punição: 2° ocorrência, BAN

[X] Ficar de zoas com quem está querendo aprender:
Punição: BAN

[X] Nudes:
Punição: 1° ocorrência, AVISO
Punição: 2° ocorrência, BAN

[X] Ofender outros membros:
Punição: 1° ocorrência, AVISO
Punição: 2° ocorrência, BAN

[+]: Divulgação de grupos, sites, etc...: [!] 1 vez a cada 2 dias. Caso o tempo acima não seja respeitado:
Punição: 1° ocorrência, AVISO
Punição: 2° ocorrência, BAN''')


@bot.message_handler(commands=['link'])
def comando_link(message):
    log(message)
    bot.reply_to(message,'https://telegram.me/joinchat/BprGcTvSrhHJIFlsjlLc5Q')

@bot.message_handler(commands=['livros'])
def comando_livros(message):
    log(message)
    if (str(message.chat.type) != 'private') and (str(message.chat.id) not in str(grupos_liberados)):
        block(message)
    else:
        bot.reply_to(message,'Link_livros')

@bot.message_handler(commands=['ide_python'])
def comando_ide_python(message):
    log(message)
    if (str(message.chat.type) != 'private') and (str(message.chat.id) not in str(grupos_liberados)):
        block(message)
    else:
        bot.reply_to(message,'http://wiki.python.org.br//IdesPython')

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
            bot.reply_to(message,'Sugestão recebida, obrigado')
        else:
            bot.reply_to(message,'Uso: /sugestão <sugestão>')
            
bot.polling()
