import re
import requests
import json
from requests.auth import HTTPBasicAuth

token = ' '
rota_base = 'http://webservicepaem-env.eba-mkyswznu.sa-east-1.elasticbeanstalk.com/api.paem/'
rec = ' '

def login(cpf, matricula, recuso):
    global token, rec
    rec = recuso
    try:
        # conexão para pegar o token (funcionado)
        headers = {"Authentication": f"CPF {cpf}"}
        response = requests.post(url=f"{rota_base}/auth.bot", headers=headers)
        res = str(response)[10:15]

        if res == '[200]':
            print("conexão iniciada")
            token = json.loads(response.content).get('token')
            resp, nome, id_discente, campus, id_recurso, id_usuario = search_id(cpf, matricula)
            if resp:
                return True, nome, id_discente, campus, id_recurso, id_usuario, token
            else:
                return False, '', '', '', '', ''

        elif res == '[401]':
            print("Não Fiz Conexão")
            return False, '', '', ''

    except EOFError:  # problema de conexão
        print("ERRO NA CONEXÃO")
        return False, '', '', '', '', ''


def search_id(cpf, matricula):
    global token
    try:
        bearer_token = f"Bearer {token}"
        payload = {"Authorization": bearer_token}
        res = requests.get(
            url=f"{rota_base}/usuarios",
            headers=payload
        )

        lista = res.json()
        my_cpf = str(cpf)

        for i in lista:
            if my_cpf in i.values():
                id_usuario = str(i['id'])
                resposta, nome, id_discente, campus, id_recurso = search_name(matricula)
                if resposta:
                    print("Usuario encontrado")
                    return True, nome, id_discente, campus, id_recurso, id_usuario, 
                else:
                    print("Usuario não encontrado")
                    return False, '', '', '','',''

    except EOFError:
        print("ERRO SEARCH_ID< EM CONEXÃO")
        return False, '', '', '','',''


def search_name(matricula):
    global token
    try:
        bearer_token = f"Bearer {token}"
        payload = {"Authorization": bearer_token}
        resp_discente = requests.get(url=f"{rota_base}/discentes", headers=payload)
        my_matric = str(matricula)
        lista2 = resp_discente.json()
        for n in lista2:
            if my_matric in n.values():
                nome = str(n['nome'])
                id_discente = str(n['id'])
                resp, campus , id_recurso = data_campus(id_discente=id_discente)
                if resp:
                    return True, nome, id_discente, campus, id_recurso

    except Exception:
        print("ERRO SEARCH_NAME< EM CONEXÃO")
        return False, '', '','',''


def data_campus(id_discente):
    global token, rec
    try:
        bearer_token = f"Bearer {token}"
        payload = {"Authorization": bearer_token}
        resp_discente = requests.get(url=f"{rota_base}/discentes/discente?id_discente={id_discente}", headers=payload)
        campus = json.loads(resp_discente.content).get('campus')

        resp_campus = requests.get(url=f"{rota_base}/recursos_campus", headers=payload)

        lista = resp_campus.json()
        #print(lista)
        rec = rec.lower()
        for n in lista:
            if rec in n.get('nome').lower():
                id_recurso = n['id']
                print("Recuso encontrado")

                return True, campus, id_recurso
                
        print("Recurso não encontrado")
        return False, '', ''
    except Exception:
        print("ERRO DATA_CAMPUS< CONEXÃO")
        return False, '', ''
 
"""recuros = "Area Comum de Convivência"
login(77777777777, 2019002845, recuros)


def envia_dados():
     pass"""

