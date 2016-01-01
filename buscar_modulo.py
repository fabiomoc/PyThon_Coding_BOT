import xmlrpc.client as xmlrpclib
client = xmlrpclib.ServerProxy('https://pypi.python.org/pypi')

def buscar_modulo(nome):
        stable = {}
        message = []
        resultados = client.search({'name': nome})
        for n in resultados: stable[n['name']] = n['version']
        for x in stable:
                message.append('\n\n[+] ' + x)
                try:
                        message.append('\nDownload: ' + client.release_data(x,stable[x])['release_url'])
                except KeyError:
                        message.append('\nNenhum Link encontrado')
        return(message)
