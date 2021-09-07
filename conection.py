import re
import requests
import json
from requests.auth import HTTPBasicAuth
from telebot.util import per_thread

token = ' '
rota_base = 'http://webservicepaem-env.eba-mkyswznu.sa-east-1.elasticbeanstalk.com/api.paem/'
#codigo erro de conexão == 0
#codigo erro usuario não encontrado == n


def login(cpf, matricula):
    global token, rec
    try:
        print("comecei")
        headers = {"Authentication": f"CPF {cpf}"}
        print("criei o header")
        response = requests.post(url=f"{rota_base}/auth.bot", headers=headers)
        print("fui e voltei")
        res = str(response)[10:15]
        print("separei a resposta")
        print(f"a resposta foi {res}")

        if res == '[200]':
            print("resposta OK")
            token = json.loads(response.content).get('token')
            return True, ''

        elif res == '[400]':
            print("resposta OK'not")
            return False, 1

    except Exception:  # problema de conexão
        print("ERRO server")
        return False, 00