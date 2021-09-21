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




from datetime import date, datetime, timedelta
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

isDate(d)