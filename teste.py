'''import re

# string de entrada
string = "03051107212"

# quebra a string, mas inclui strings vazias
lista = re.split("(\S{3})", string)



# remove strings vazias, deixa apenas o que interessa
final = list(filter(None, lista))

print(final)'''

#teste = input("CPF: ") # 12345678900


'''
l = [{'nome': 'Laboratório de ensino em Biologia', 'id': 1, 'inicio_horario': '08:00:00', 'fim_hoario': '08:00:00'}, {'nome': 'Laboratório multidisciplinar de biologia II', 'id': 2, 'inicio_horario': '08:00:00', 'fim_hoario': '08:00:00'}, {'nome': 'Laboratório de Informática', 'id': 3, 'inicio_horario': '08:00:00', 'fim_hoario': '08:00:00'}, {'nome': 'Sala de Aula Inteligente I', 'id': 4, 'inicio_horario': '08:00:00', 'fim_hoario': '08:00:00'}, {'nome': 'Sala de Aula Inteligente II', 'id': 5, 'inicio_horario': '08:00:00', 'fim_hoario': '08:00:00'}, {'nome': 'Biblioteca', 'id': 6, 'inicio_horario': '14:00:00', 'fim_hoario': '14:00:00'}, {'nome': 'Area Comum de Convivência', 'id': 7, 'inicio_horario': '08:00:00', 'fim_hoario': '08:00:00'}, {'nome': 'Auditorio', 'id': 8, 'inicio_horario': '08:00:00', 'fim_hoario': '08:00:00'}, {'nome': 'Carteirinha', 'id': 9, 'inicio_horario': '08:00:00', 'fim_hoario': '08:00:00'}, {'nome': 'Chips Claro - Projeto Alunos Conectados', 'id': 10, 'inicio_horario': '08:00:00', 'fim_hoario': '08:00:00'}]
cont = 0
o = ""
for i in l:
    o = f"{o}\n{str(i['id'])} - {str(i['nome'])}"
    cont+=1

o = o + "\n"

a = int(f"{input(o)}")



for i in l:
    compare = int(i['id'])
    if a == compare:
        print("Valido")
        break
    
    print("Invalido")'''



'''horaIni = "08:00:00"
horaFim = "18:00:00"

ini = int(horaIni[0:2])
fim = int(horaFim[0:2])

menuHour = ""
mark = 1

ant = ini

while ant < fim:
    menuHour = f"{menuHour}\n {mark} - {ant}:00 as {ant+2}:00"
    ant+=2
    mark+=1

print(menuHour)
print(mark - 1)'''

'''horaUser = '18:00 as 22:00'


horaios = {'08:00 as 10:00','10:00 as 12:00', '14:00 as 16:00', 
            '16:00 as 18:00', '18:00 as 20:00', '20:00 as 22:00'}


if horaUser in horaios:
    print("Valido")
else:
    print("Invalido")'''




"""from datetime import date, datetime, timedelta
import datetime

def isDate(data_user):
    try:
        data_ = str(data_user).split("/")

        dia = int(data_[0])
        mes = int(data_[1])
        ano = int(data_[2])

        newDate = datetime.date(ano, mes, dia)

        data_limite = date.today() + timedelta(days=2)

        if newDate >= date.today():
            if newDate <= data_limite:

                print("Valido") #é uma data, é menor que dois dias

            else:
                print("Acima") #é uma data, é maior que dois dias

        else:

            print("Abaixo") #data anterior a hoje
        
    except Exception:
        print("Deu merda") #não é uma data


d = "24/12/2000"

isDate(d)"""



"""for e in range(3):
    pas = open("teste.txt", "a")
    i = input("Digite um nome:")
    pas.write(f"Nome: {i}\t")
    p = input("Digite sua idade: ")
    pas.write(f"Idade: {p}\n")
    pas.close()


lines = []
with open("teste.txt") as f:
    lines = f.readlines()
print(lines)
count = 0"""




"""dados_aluno = {          "para_si": int(aluno.para_si), OK
                            "data": aluno.data, ok
                            "hora_inicio": f"{aluno.hora_inicio}:00", ok
                            "hora_fim": f"{aluno.hora_fim}:00", ok
                            "status_acesso": 1, ok
                            "nome": aluno.nome, ok
                            "fone": aluno.telefone, ok
                            "cpf": aluno.cpf, ok
                            "usuario_id_usuario": int(aluno.id_usuario), ok
                            "discente_id_discente": int(aluno.id_discente),
                            "recurso_campus_id_recurso_campus": aluno.id_recurso}

            agendar(dados_aluno, token, chat_id)
        
    except Exception:
        pass
      

def agendar(lista, token, chat_id):
    
    headers = {"Authorization":f"Bearer {token}", "Content-Type": "application/json"}
    url = "http://webservicepaem-env.eba-mkyswznu.sa-east-1.elasticbeanstalk.com/api.paem/"
    resp = requests.post(url+"/solicitacoes_acessos/solicitacao_acesso", data=json.dumps(lista),headers=headers)
    
    res = str(resp)[10:15]

    print(res)
    
    if res == "[201]":
        print(lista)
        bot.send_message(chat_id, f"Certo, a reserva de {aluno.nome} foi feita com sucesso")

    elif res == "[500]":
        bot.send_message(chat_id, "Esse discente já reservou essa sala, ou o horario solicitado não está disponivel para atendimento")
    
    elif res == "[400]":
        bot.send_message(chat_id, "ERRO NO SERVIDOR")

    elif res == "[405]":
        bot.send_message(chat_id, "ERRO NO METODO")"""


#id_rec = bot.get_updates()[-1].message.text

"""
import datetime


data_user = "05/10/2021"

import json

import requests


token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJsb2dpbiI6Im1hcmNrIiwiZXhwIjoxNjMzNDc4NTYxfQ.9pdVVFNVanEaWXhVSoT5GFMB6aoL9KttQ6LaDEtyaxg"
dicionario = dict()
arq = open("1832638103.text", "r") 
linhas = arq.read()
dados = linhas.split("!")

dados.remove("")

for i in dados:
    dados = i.split(";")
    dicionario[dados[0]] = dados[1]


dicionario['data'] = "05-10-2021"

dados_aluno = {          "para_si": dicionario['para_si'],
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
#tranformar em json"""




"""
from time import sleep
import os
usuario = 1832638103
p = str(usuario)
arc = open(p + ".txt", "w")
#sleep(1)
arc.__del__()
os.remove(p+".txt")"""



"""#Ajuste do telefone para usar o phonenumbers
def verificPhone(phone):
    cond=''
    telefone_teste= phone
    ddd= phone[0:4]

    if '(' in telefone_teste  and ')' in telefone_teste and '-' in telefone_teste and len(telefone_teste)>=14 and len(telefone_teste)< 16:
        cond=True
    else:
        cond=False
    
    return cond


num = '(93) 99122-6497'
r = verificPhone(num)
print(r)"""

"""import re

pattern = r"^(\d{2})(\d?)(\d{4})(\d{4})$"

if re.match(pattern, input()):
    print("Valid")
else:
    print("Invalid")"""




dados_aluno = {
    'recurso_campus_id_recurso_campus' = 1,
    'data' =>  $newdata,
    'hora_inicio' => $hi_hf[0],
    'hora_fim' => $hi_hf[1],
    'nome' =>  strtoupper(addslashes($_POST['nome'])),
    'discente_id_discente' => strval( addslashes($_POST['id_disc'])),
    'para_si' => 1,
    'status_acesso' => 1
  
 }
        

        print(dados_aluno)
        headers = {"Authorization":f"Bearer {token}"}
        resp = requests.post(f"{rota_base}/solicitacoes_acessos/solicitacao_acesso", data=json.dumps(dados_aluno),headers=headers)
        print(resp)
        res = str(resp)[10:15]
        print(res)