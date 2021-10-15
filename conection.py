import requests
import json
import dados_bot
from datetime import date, datetime


from botUtil import writeText, makeMenu, removeFile, makeDictionary


token = ' '
rota_base = dados_bot.rota_base


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

        if res == '[200]': #LIGIN EFETUADO

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
            

def getHora(idRecUser, user):
    try:
        hora=dict()

        bearer_token = f"Bearer {token}"
        payload = {"Authorization": bearer_token}
        resp_campus = requests.get(url=f"{rota_base}/recursos_campus/recurso_campus?id_recurso_campus={idRecUser}", headers=payload)
        recurso = resp_campus.json()

        horaIni = recurso['inicio_horario_funcionamento']
        horaFim = recurso['fim_horario_funcionamento']
        capacidade = recurso['capacidade']

        writeText(user, 'capacidade', capacidade)

        
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



def verificCapacity(user):
    print("chegeui")
    bearer_token = f"Bearer {token}"
    payload = {"Authorization": bearer_token}
    suporte=0
    capacidade=0

    dicionario = makeDictionary(user)
    id_recurso = int(dicionario["recurso_campus_id_recurso_campus"])
    capacidade = int(dicionario['capacidade'])

    data_user = dicionario['data']
    horaIni = dicionario['hora_inicio']
    horaFim = dicionario['hora_fim']
    
    resp_solicitacao = requests.get(url=f"{rota_base}/solicitacoes_acessos", headers=payload)
    json_solicitacao = resp_solicitacao.json()

    for i in json_solicitacao:
        idRecurso = int(i['recurso_campus_id_recurso_campus'])
        if id_recurso == idRecurso:
            data_old = datetime.strptime(str(i['data']), '%Y-%m-%d').date()
            dataFormatada = data_old.strftime('%d-%m-%Y')
            if data_user in str(dataFormatada):
                if horaIni in str(i["hora_inicio"]) and horaFim in str(i['hora_fim']):
                    suporte+=1
 
    if suporte >= capacidade:
        return False
    else:
        return True



def makeReservation(user):
    try:
        writeText(user, "status_acesso", "1")

        dicionario = makeDictionary(user)
        
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
        resp = requests.post(url+"/solicitacoes_acessos/solicitacao_acesso", data=json.dumps(dados_aluno),headers=headers)
        res = str(resp)[10:15]
        
        if res == "[201]":

            removeFile(user)
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

