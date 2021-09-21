from time import sleep
import requests
import json


token = ' '
rota_base = 'http://webservicepaem-env.eba-mkyswznu.sa-east-1.elasticbeanstalk.com/api.paem/'


''' ### codigos erros ### 
    conexão no cpf == 0
    cpf não encontrado == 1
    matricula não encontrada == 2
    conexão matricula == 3
    id não encontrado == 4
    id invalido == 5'''


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
        
        for i in lista:
            if matricula in i.values():
                nome_discente = str(i['nome'])
                id_discente = str(i['id'])
                matricula_discente = str(i['matricula'])
                
                resp_discente = requests.get(url=f"{rota_base}/discentes/discente?id_discente={id_discente}", headers=payload)
                campus_id_discente = json.loads(resp_discente.content).get('campus_id_campus')

                resp_campus_recursos = requests.get(url=f"{rota_base}/recursos_campus", headers=payload)
                lista_recurso = resp_campus_recursos.json()
                
                protocolo = getProtocol()
                backupDados(protocolo, nome_discente)
                backupDados(protocolo, id_discente)
                backupDados(protocolo, matricula_discente)
                backupDados(protocolo, campus_id_discente)
                backupDados(protocolo, lista_recurso)

                return True, '', lista_recurso
        
        return False, 2, ''

    except Exception:
        return False, 3, ''



def verific_id(id):
    try:
        bearer_token = f"Bearer {token}"
        payload = {"Authorization": bearer_token}
        resp_campus = requests.get(url=f"{rota_base}/recursos_campus", headers=payload)
        recursos = resp_campus.json()

        for i in recursos:
            compare = int(i['id'])
            if id == compare:
                return True, '', ''
        
        menu = criaMenu(recursos)
        return False, 4, menu
    
    except Exception:
        meni = criaMenu(recursos)
        return False, 5, meni


def criaMenu(recurso):
    msg = "Selecinone o Numero da opção\n"
    for i in recurso:
        msg = f"{msg}\n{str(i['id'])} - {str(i['nome'])}"
    
    return msg
            

def getHora(idRecUser, id_chat):
    try:
        bearer_token = f"Bearer {token}"
        payload = {"Authorization": bearer_token}
        resp_campus = requests.get(url=f"{rota_base}/recursos_campus/recurso_campus?id_recurso_campus={idRecUser}", headers=payload)
        recurso = resp_campus.json()

        horaIni = recurso['inicio_horario_funcionamento']
        horaFim = recurso['fim_horario_funcionamento']

        ini = int(horaIni[0:2])
        fim = int(horaFim[0:2])

        menuHour = ""
        ant = ini
        dot = 0

        while ant < fim:
            if dot == 2:
                ant+=2

            else:
                menuHour = f"{menuHour}\n{ant}:00 as {ant+2}:00"
                ant+=2
            dot+=1

        return menuHour, id_chat, idRecUser

    except Exception:
        pass


def backupDados(protocolo_usuario, dadoParaSalvar):
    if dadoParaSalvar == "NULL" or protocolo_usuario == "NULL":
        #primeira mensagem
        pass


def makeReservation():
    para_si, data, hora_inicio, hora_fim, phone, nome, cpf, id_usuario, id_discente, id_recurso= getAlldata()

    

def getProtocol():
    #ir no banco e voltar com o protocolo
    pass

def getAlldata():
    pass #função para recuperar todos os dados do usuario


def getDados(protocolo, dadosParaRecuperar):
    #pegar algum dado
    pass