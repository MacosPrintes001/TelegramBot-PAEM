from email import header
from lib2to3.pgen2.token import RPAR
import this
import requests
import json
from dados_bot import rota_base
from botUtil import writeText, makeMenu, removeFile


token = ' '


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
        response = requests.post(url=f"{rota_base}/auth.bot", headers=headers) #ENTRA NA ROTA AUTH.BOT PARA REALIZAR LOGIN
        res = str(response)[10:15]

        if res == '[200]': #LOGIN EFETUADO

            token = json.loads(response.content).get('token')
            bearer_token = f"Bearer {token}"
            payload = {"Authorization": bearer_token}
            res = requests.get(url=f"{rota_base}/usuarios",headers=payload)
            lista = res.json()

            for i in lista: #PERCORRE JSON
                if cpf in i.values(): #SE CPF EM JSON USUARIOS
                    #PEGANDO DADOS DO USUARIO E ESCERVENDO NO ARQIUVO TXT
                    id_usuario = str(i['id'])
                    writeText(user, "cpf", cpf)
                    writeText(user, "usuario_id_usuario", id_usuario)
                   
                    return True, ''

        elif res == '[400]': #CPF NÃO ENCONTRADO
            return False, 1

    except Exception:  #PROBLEMA NA CONEXÃO
        return False, 0



def dadosUsuario(matricula, user):
    global token
    try:
        bearer_token = f"Bearer {token}"
        payload = {"Authorization": bearer_token}
        resp_discente = requests.get(url=f"{rota_base}/discentes", headers=payload) #ACESSANDO ROTA DISCENTE
        lista = resp_discente.json()
        
        for i in lista: #PERCORRE DISCENTES
            if matricula in i.values(): #SE MATRICULA EM JSON DISCENTES

                #CAPTURA E ESCREVE OS DADOS DO USUARIO NO TXT
                nome_discente = str(i['nome'])
                id_discente = str(i['id'])
                matricula_discente = str(i['matricula'])
                writeText(user, "nome", nome_discente)
                writeText(user, "discente_id_discente", id_discente)
                writeText(user, "matricula", matricula_discente)
                
                #ACESSA A ROTA DOS RECURSOS
                resp_campus_recursos = requests.get(url=f"{rota_base}/recursos_campus", headers=payload)
                lista_recurso = resp_campus_recursos.json()
                menu_recursos, dados = makeMenu(lista_recurso) #CRIA UM MENU COM OS RECURSOS PARA MOSTRAR AO USUARIO

                return True, dados, menu_recursos
        
        return False, 2, '' #MATRICULA NÃO ENCONTRADA

    except Exception:
        return False, 3, '' #USUARIO ENVIU UM CARACTERE DESCONEHCIDO



def verific_id(recurso_user): #FAZ A VERIFICAÇÃO DA OPÇÃO ESCOLHIDA PELO USUARIO
    try:
        global token

        recurso = str(recurso_user)
        comprimento = len(recurso)
        id = recurso[comprimento-2] + recurso[comprimento-1] #EXTRAI O ID DO RECURSO ESCOLHIDO
        id = int(id)
        
        bearer_token = f"Bearer {token}"
        payload = {"Authorization": bearer_token}
        resp_campus = requests.get(url=f"{rota_base}/recursos_campus", headers=payload)
        recursos = resp_campus.json()

        for i in recursos: #PERCORRE JSON DE RECURSOS
            compare = int(i['id'])
            if id == compare: #VERIFICA 
                return True, '', '', id
        
        menu, dados = makeMenu(recursos)
        return False, 4, menu, dados
    
    except Exception:
        meni, dados = makeMenu(recursos)
        return False, 5, meni, dados
            

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
                menuHour = f"{menuHour}\n{cont} - {ant}:00 as {ant+2}:00"
                #INSERE NO DICIONARIO AS HORAS REFERENTE AO RECURSO ESCOLHIDO
                hora[cont]=f"{ant}:00 as {ant+2}:00"
                ant+=2
    
            dot+=1

        return menuHour, hora

    except Exception:
        pass


def makeReservation(user):
    try:
        global token
        writeText(user, "status_acesso", "1")

        dicionario = dict()
        arq = open(user+".txt", "r")
        linhas = arq.read()
        dados = linhas.split("!")
        dados.remove("")
        for i in dados:
            dados = i.split(";")
            dicionario[dados[0]] = dados[1]
        arq.close()
        
        dados_aluno = { 
                        "para_si": dicionario["para_si"],
                        "data": dicionario["data"],
                        "hora_inicio":dicionario["hora_inicio"],
                        "hora_fim":dicionario["hora_fim"],
                        "status_acesso":dicionario["status_acesso"],
                        "nome":dicionario["nome"],
                        "fone":dicionario["fone"],
                        "usuario_id_usuario": int(dicionario["usuario_id_usuario"]),
                        "discente_id_discente": dicionario["discente_id_discente"],
                        "recurso_campus_id_recurso_campus":dicionario["recurso_campus_id_recurso_campus"]}



        fData = json.dumps(dados_aluno)
        header = {"content-Type": "application/json","Authorization": f"Bearer {token}"}
        print(header)
        resp =  requests.post(url=f"{rota_base}/solicitacoes_acessos/solicitacao_acesso", data=fData, headers=header)
        
        print(resp.json())
        res = str(resp)[10:15]
        if res == "[201]":
            print("Tudo certo")
            removeFile(user)
            return True
        else:
            return False

    except Exception:
        print("Deu erro")
        return False



