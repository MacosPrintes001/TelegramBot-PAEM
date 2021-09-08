import re
from time import sleep
import requests
import json
from requests.api import get
from requests.auth import HTTPBasicAuth
from telebot.util import per_thread

token = ' '
rota_base = 'http://webservicepaem-env.eba-mkyswznu.sa-east-1.elasticbeanstalk.com/api.paem/'


''' ### codigos erros ### 
    conexão no cpf == 0
    cpf não encontrado == 1
    matricula não encontrada == 2
    conexão matricula == 3'''


def login(cpf):
    global token
    try:
        headers = {"Authentication": f"CPF {cpf}"}
        response = requests.post(url=f"{rota_base}/auth.bot", headers=headers)
        res = str(response)[10:15]

        if res == '[200]':
            token = json.loads(response.content).get('token')
            
            bearer_token = f"Bearer {token}"
            payload = {"Authorization": bearer_token}
            res = requests.get(url=f"{rota_base}/usuarios",headers=payload)
            lista = res.json()
            for i in lista:
                if cpf in i.values():
                    sleep(3)
                    id_usuario = str(i['id'])
                    protocolo = getProtocol()
                    backupDados(protocolo, id_usuario)
                    backupDados(protocolo, cpf)
                   
                    return True, ''

        elif res == '[400]':
            return False, 1

    except Exception:  # problema de conexão
        return False, 0



def dadosUsuario(matricula):
    global token
    try:
        bearer_token = f"Bearer {token}"
        payload = {"Authorization": bearer_token}
        resp_discente = requests.get(url=f"{rota_base}/discentes", headers=payload)
        lista = resp_discente.json()

        print(lista)
        
        for i in lista:
            if matricula in i.values():
                nome = str(i['nome'])
                id_discente = str(i['id'])

                sleep(2)
                protocolo = getProtocol()
                backupDados(protocolo, nome)
                backupDados(protocolo, id_discente)
                backupDados(matricula)

                return True, ''
                '''resp, campus , id_recurso = data_campus(id_discente=id_discente)
                if resp:
                    return True'''
        
        return False, 2

    except Exception:
        return False, 3



def backupDados(protocolo_usuario, dadoParaSalvar):
    if dadoParaSalvar == "NULL" or protocolo_usuario == "NULL":
        #primeira mensagem
        print("protocolo enviado ao banco")

def getProtocol():
    #ir no banco e voltar com o protocolo
    pass

def getDados(protocolo):
    #pegar algum dado
    pass