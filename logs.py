from datetime import datetime
import ast

def log_erros(func, erro, mensagem):
    arquivo_logs = open('Logs_de_erros.txt', 'a')
    arquivo_logs.write('''

#Erro! Função {fun} {data}
Mensagem de erro:
{log_erro}
Mensagem que originou o erro:
{mensagem}
------------------------------------'''
                  .format(fun = func, data = str(datetime.today()), log_erro = erro,
                          mensagem = str(mensagem).encode('UTF-8', errors='ignore').decode('ASCII', errors='ignore')))
        
    arquivo_logs.close()
    

def log_msg(dados_msg):
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
