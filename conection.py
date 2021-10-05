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


arc = ""
def login(cpf, user):
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

                    id_usuario = str(i['id'])

                    arc = open(user+".txt", "a") #CRIARNDO ARQIVO TXT
                    arc.write(f"CPF: {cpf}\n")
                    arc.write(f"ID_USUARIO: {id_usuario}\n")
                    arc.close()
                    
                    """backupDados(protocolo, id_usuario)
                    backupDados(protocolo, cpf)"""
                   
                    return True, ''

        elif res == '[400]':
            return False, 1

    except Exception:  # problema de conexão
        return False, 0



def dadosUsuario(matricula, user):
    global token
    dados = dict()
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

                cont = 1
                for i in lista_recurso:
                    menu_recuso = ""
                    dados[cont] = f"{cont} - {str(i['nome'])} {int(i['id'])}"
                    menu_recuso = menu_recuso + f"{cont} - {str(i['nome'])}"
                    cont+=1

                arc = open(user+".txt", "a")
                arc.write(f"NOME: {nome_discente}\n")
                arc.write(f"ID_DISCENTE: {id_discente}\n")
                arc.write(f"MATRICULA: {matricula_discente}\n")
                arc.close()
                

                return True, dados, menu_recuso
        
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
            

def getHora(idRecUser):
    try:
        hora=dict()
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
        cont = 0

        while ant < fim:
            cont+=1
            if dot == 2:
                ant+=2
                cont-=1

            elif dot == 1:
                menuHour = f"{menuHour}\n{cont} - 0{ant}:00 as {ant+2}:00"
                #INSERE NO DICIONARIO AS HORAS REFERENTE AO RECURSO ESCOLHIDO
                hora[cont]=f"{ant}:00 as {ant+2}:00"

            else:
                menuHour = f"{menuHour}\n{cont} - {ant}:00 as {ant+2}:00"
                #INSERE NO DICIONARIO AS HORAS REFERENTE AO RECURSO ESCOLHIDO
                hora[cont]=f"{ant}:00 as {ant+2}:00"
                ant+=2
            dot+=1
        return menuHour, hora

    except Exception:
        pass


def backupDados(protocolo_usuario, dadoParaSalvar):
    if dadoParaSalvar == "NULL" or protocolo_usuario == "NULL":
        #primeira mensagem
        pass


def makeReservation(user):
    #para_si, data, hora_inicio, hora_fim, phone, nome, cpf, id_usuario, id_discente, id_recurso = getAlldata()

    arc = open(user+".txt", "r")
    linhas = arc.readlines()
    out_file  = open(user+".json", "w")
    json.dump(linhas, out_file)
    arc.close()
    out_file.close()

    """headers = {"Authorization":f"Bearer {token}", "Content-Type": "application/json"}
    url = "http://webservicepaem-env.eba-mkyswznu.sa-east-1.elasticbeanstalk.com/api.paem/"
    resp = requests.post(url+"/solicitacoes_acessos/solicitacao_acesso", data=json.dumps(lista),headers=headers)
    
    res = str(resp)[10:15]
    
    if res == "[201]":
        return "OK"

    elif res == "[500]":
        return "NOT"#aluno já reservou este local

    elif res == "[400]":
        return 'NOT' #erro no servidor

    elif res == "[405]":
        return 'NOT' #erro no metodo"""


def getProtocol():
    #ir no banco e voltar com o protocolo
    pass


def getAlldata():
    pass #função para recuperar todos os dados do usuario


def getDados(protocolo, dadosParaRecuperar):
    #pegar algum dado
    pass