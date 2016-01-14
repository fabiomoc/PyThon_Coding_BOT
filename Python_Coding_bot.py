# -*- coding: UTF-8 -*-
#!/usr/bin/python3

import telebot, ast, re, requests
from buscar_modulo import buscar_modulo
from datetime import datetime


token = '<token>'
bot = telebot.TeleBot(token)
staff = -94082849

grupos_liberados = ['-74638594','-1001003662865', '-44624117']
IDs_liberados = [110806640]
grupos_monitorados = ['-74638594','-1001003662865', '-44624117']
administradores = {-1001003662865: '''Administradores do Grupo: Python Coding - BS|EH
@EXPL01T3R0
@B1zzy1
@Ftimoteo
@gilmar_soares
@washings
@marcoantonio650
@Duarte10
@W0RMGU1M4
@AnDroidEL
@andersonmv
@Somyoshi
@devmaker
@laenderoliveira
''', -94082849: '''Administradores do Grupo: Python Coding Staff
@EXPL01T3R0
@B1zzy1
@Ftimoteo
@gilmar_soares
@washings
@marcoantonio650
@Duarte10
@W0RMGU1M4
@AnDroidEL
@andersonmv
@Somyoshi
@devmaker
@laenderoliveira'''}

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
    global msg
    msg = dados_msg
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
        print('\n------------------------------------\nErro na função log, consulte o arquivo logs_de_erros,', datetime.today())
        
def block(mensagem):
    bot.reply_to(mensagem,'''
Este bot esta programado para funcionar somente no grupo Python Coding - BS|EH
Entre para o grupo usando este link: https://telegram.me/joinchat/BprGcTvSrhHJIFlsjlLc5Q

Para conseguir autorização para este chat, entre em contato com meu desenvolvedor, @EXPL01T3R0''')

@bot.message_handler(commands=['adm', 'admin','admins', 'administradores', 'administrators', 'mod', 'moderadores', 'mods'])
def adm(mensagem):
    try:
        if administradores.get(mensagem.chat.id):
            bot.reply_to(mensagem, administradores.get(-1001003662865))
        else:
            bot.reply_to(mensagem, '''A lista de administradores não esta configurada neste grupo
Caso queira incluir a lista de administradores deste grupo, entre em contato com meu desenvolvedor, @EXPL01T3R0 ''')
    except Exception as erro:
        log_erros('admin', erro, mensagem)
        print('\n------------------------------------\nErro na função admin, consulte o arquivo logs_de_erros,', datetime.today())
            

@bot.message_handler(commands=['id'])
def id_(mensagem):
    log(mensagem)
    try:
        bot.reply_to(mensagem,'''
ID
Seu Nome: {nome}
Username: @{username}
ID:       {id_user}
---------------------
Nome do Chat: {nome_grupo}
ID do Grupo:   {id_grupo}'''.format(nome = mensagem.from_user.first_name + mensagem.from_user.last_name if mensagem.from_user.last_name else mensagem.from_user.first_name,
                                    username = mensagem.from_user.username, id_user = mensagem.from_user.id, nome_grupo = mensagem.chat.title,
                                    id_grupo = mensagem.chat.id))
    except Exception as erro:
            log_erros('ID', erro, mensagem)
            print('\n------------------------------------\nErro na função ID, consulte o arquivo logs_de_erros,', datetime.today())


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
            print('\n------------------------------------\nErro na função buscar_modulo, consulte o arquivo logs_de_erros,', datetime.today())



@bot.message_handler(commands=['ajuda', 'help'])
def comando_help(message):
    log(message)
    bot.reply_to(message,'''
/buscar_modulo - <termo de busca> Realiza uma busca por modulos python (ex.: /buscar_modulos telegram)

/ide_python - Exibe links de IDEs python, gratuitas e proprietárias

/livros - Exibe o link da biblioteca de livros e apostilas sobre python do grupo

/link - Exibe o Link de convite para acesso ao grupo

/help | /ajuda - Exibe a lista de comandos ativos

/regras | /rules - Exibe as regras vigentes no grupo

/Sobre | /about | /contribuir - Exibe informações sobre o bot e como contruir com o mesmo

/sugestão | /sugestao <texto> - Envie sugestões de melhorias para o bot

/id - Exibe informações sobre seu usuário e sobre o grupo atual

/admins - Exibe os administradores do grupo atual

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

[!]: Divulgação de grupos, sites, etc...:
SOMENTE COM AUTORIZAÇÃO DO ADM @EXPL01T3R0 . caso não seja respeitada a regra:
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
        bot.reply_to(message,'Link')

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
            
@bot.message_handler(commands=['sobre', 'about', 'contribuir'])
def comando_sobre(message):
    log(message)
    bot.reply_to(message,'''
PyCoding BOT v.1.0
Bot Oficial do grupo Python Coding - BS|EH
Desenvolvido por @EXPL01T3R0
Contribua ;) : https://github.com/diego-bernardes/PyThon_Coding_BOT
''')

@bot.message_handler(func=lambda mensagem: True, content_types=['new_chat_participant'])
def mensagem(mensagem):
    bot.reply_to(mensagem, '''
Bem Vindo ao Grupo Pyhon Coding - Maior grupo de Python em PT-br do telegram

Leia as regras antes de postar, envie /regras ou /rules

Se precisar de ajuda, envie /ajuda ou /help''')    
    
@bot.message_handler(func=lambda message: True)
def spam(mensagem):
    global msg
    msg = mensagem
    if (str(mensagem.chat.id) in str(grupos_monitorados)):
        links = re.findall('\w+\.\w+\w+\.\w+\/\w+\/\w+|\w+\.\w+\w+\.\w+\/\w+|\w+\.\w+\/\w+\/\w+|\w+\.\w+\/\w+',mensagem.text)
        for link in links:
            resolve = requests.get('http://api.longurl.org/v2/expand?url='+str(link)).content.decode()
            #resolve = re.search('(<\!\[CDATA\[)(.*?)(\]\]\>\<\/long-url>)', resolve)
            if re.search('(telegram.me|joinchat|)', resolve) and str(mensagem.from_user.id) not in str(IDs_liberados):
                user = mensagem.from_user.id
                try: log_ban = ast.literal_eval(open('log_ban').read())
                except: log_ban = {}
                if log_ban.get(user):
                    log_ban[user] +=1
                    if log_ban.get(user) >= 2:
                        bot.reply_to(mensagem,'''
Divulgação não autorizada!
você já foi alertado sobre isso, portanto, pedirei a um administrador que remova você!''')
                        bot.send_message(staff, '''
Onde estão os admin ça poha?
Estão fazendo divulgação no grupo! !

Ele já havia sido avisado, então alguém bane ele por favor, eu não sei fazer isso''')
                        bot.forward_message(staff, mensagem.chat.id, mensagem.message_id)
                else:
                    log_ban[user] = 1
                    bot.reply_to(mensagem, '''
Divulgação não autorizada!
Seu nome de usuário foi registrado na lista de observação e caso volte a divulgar algum grupo/canal sem autorização, você será banido

Para obter autorização para divulgação fale com algum administrador, para ver quem são so administradores do grupo, digite /adm

Leia as regras do grupo antes de postar''')
                with open('log_ban', 'w') as salvar_log: salvar_log.writelines(str(log_ban))
                bot.send_message(staff, '''
Onde estão os admin ça poha?
Estão fazendo divulgação no grupo! !
Dei um aviso pra ele, na segunda, ele vai ser banido !

Só falta alguém ir la e excluir a mensagem, porque eu não sei como fazer isso''')
                bot.forward_message(staff, mensagem.chat.id, mensagem.message_id)

print('Bot Iniciado')        
bot.polling()
