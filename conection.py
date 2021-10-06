import requests
import json

from botUtil import writeText


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
                    writeText(user, "cpf", cpf)
                    writeText(user, "usuario_id_usuario", id_usuario)
                   
                    return True, ''

        elif res == '[400]':
            return False, 1

    except Exception:  # problema de conexão
        return False, 0



def dadosUsuario(matricula, user):
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

                menu_recursos, dados = criaMenu(lista_recurso)

                writeText(user, "nome", nome_discente)
                writeText(user, "discente_id_discente", id_discente)
                writeText(user, "matricula", matricula)
                #writeText(user, "matricula", matricula_discente)

                return True, dados, menu_recursos
        
        return False, 2, ''

    except Exception:
        return False, 3, ''



def verific_id(recurso_user):
    try:

        print(recurso_user)
        recurso = str(recurso_user)
        comprimento = len(recurso)
        id = recurso[comprimento-2] + recurso[comprimento-1]
        id = int(id)
        

        print(id)

        bearer_token = f"Bearer {token}"
        payload = {"Authorization": bearer_token}
        resp_campus = requests.get(url=f"{rota_base}/recursos_campus", headers=payload)
        recursos = resp_campus.json()

        for i in recursos:
            compare = int(i['id'])
            if id == compare:
                return True, '', '', id
        
        menu, dados = criaMenu(recursos)
        return False, 4, menu, dados
    
    except Exception:
        meni, dados = criaMenu(recursos)
        return False, 5, meni, dados


def criaMenu(lista_recurso):
    dados = dict()
    menu_recuso = "Selecinone o Numero da opção\n"
    cont = 1
    for i in lista_recurso:
        dados[cont] = f"{cont} - {str(i['nome'])} {int(i['id'])}"
        menu_recuso = f"{menu_recuso}\n{cont} - {str(i['nome'])}"
        cont+=1

    return menu_recuso, dados
            

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

            else:
                if dot == 0:
                    menuHour = f"{menuHour}\n{cont} - 0{ant}:00 as {ant+2}:00"
                    #INSERE NO DICIONARIO AS HORAS REFERENTE AO RECURSO ESCOLHIDO
                    hora[cont]=f"0{ant}:00 as {ant+2}:00"
                    ant+=2

                else:
                    menuHour = f"{menuHour}\n{cont} - {ant}:00 as {ant+2}:00"
                    #INSERE NO DICIONARIO AS HORAS REFERENTE AO RECURSO ESCOLHIDO
                    hora[cont]=f"{ant}:00 as {ant+2}:00"
                    ant+=2

            dot+=1

        print(hora)
        return menuHour, hora

    except Exception:
        pass


def backupDados(protocolo_usuario, dadoParaSalvar):
    if dadoParaSalvar == "NULL" or protocolo_usuario == "NULL":
        #primeira mensagem
        pass


def makeReservation(user):
    try:
        writeText(user, "status_acesso", "1")

        dicionario = dict()
        arq = open(user+".text", "r") 
        linhas = arq.read()
        dados = linhas.split("!")
        dados.remove("")
        for i in dados:
            dados = i.split(";")
            dicionario[dados[0]] = dados[1]

        
        dados_aluno = {  "para_si": dicionario['para_si'],
                        "data": dicionario['data'],
                        "hora_inicio":dicionario['hora_inicio'],
                        "hora_fim": dicionario['hora_fim'],
                        "status_acesso": dicionario['status_acesso'],
                        "nome": dicionario['nome'],
                        "fone": dicionario['fone'],
                        "cpf": dicionario['cpf'],
                        "usuario_id_usuario": dicionario['usuario_id_usuario'],
                        "discente_id_discente": dicionario['discente_id_discente'],
                        "recurso_campus_id_recurso_campus": dicionario['recurso_campus_id_recurso_campus']}


        headers = {"Authorization":f"Bearer {token}", "Content-Type": "application/json"}
        url = "http://webservicepaem-env.eba-mkyswznu.sa-east-1.elasticbeanstalk.com/api.paem"
        print("Indp na API")
        resp = requests.post(url+"/solicitacoes_acessos/solicitacao_acesso", data=json.dumps(dados_aluno),headers=headers)
        print("Voltei")
        res = str(resp)[10:15]
        print(res)
        
        if res == "[201]":
            return True

        elif res == "[500]":
            return False#aluno já reservou este local

        elif res == "[400]":
            return False #erro no servidor

        elif res == "[405]":
            return False #erro no metodo"""
        return True

    except Exception:
        return False
