from datetime import datetime
import datetime
import os
from time import sleep

arc = ""

def isTime(horarios, numb, user): #Se preciar de tempo maior é só dividir horaIni e horaFim e verificar se algum esta em horarios

    t = False
    horario = ''
    try:
        horario = horarios[numb]
        t = True
    except:
        pass

    if t:
            #alterar
        horaIni, _, horaFim = str(horario).split(" ")

        writeText(user, "hora_inicio", f"{horaIni}:00")
        writeText(user, "hora_fim", f"{horaFim}:00")

        return True
    else:
        return False


def verificPhoneNumber(phoneNumber, user):

    numeroCelular = phoneNumber
    try:
        if len(numeroCelular) != 11:
            raise ValueError
        else:

            numeroCelular = int(numeroCelular)# se contiver letras causa um ValueError
            numeroCelular = str(numeroCelular)

            celular = numeroCelular
            telFormatado = f"({celular[0:2]}) {celular[2]} {celular[3:7]}-{celular[7:]}"

            writeText(user, "fone", telFormatado)

            return True #numero valido

    except ValueError:
        if len(numeroCelular) == 0:
            return False #não digitou um numero
        else:
            return False #numero invalido


def writeText(user, key, value): #CRIA E ESCREVE NO ARQUIVO TXT OS DADOS
    """
    USER: ID DE USUARIO DO TELEGRAM
    KEY: NOME DA CHAVE QUE VAI GUARDAR O VALOR
    VALUE: DADO A SER ESCRITO NO ARQUIVO
    """
    arc = open(user+".txt", "a")
    arc.write(f"{key};{value}!")
    arc.close()


def removeFile(usuario):
    p = str(usuario)
    if os.path.exists(p+".txt"):
        os.remove(p+".txt")



def makeMenu(lista_recurso): #CRIA MENU COM OS RECURSOS
    dados = dict()
    menu_recuso = "Selecinone o Numero da opção\n"
    cont = 1
    for i in lista_recurso:
        dados[cont] = f"{cont} - {str(i['nome'])} {int(i['id'])}"
        menu_recuso = f"{menu_recuso}\n{cont} - {str(i['nome'])}"
        cont+=1

    return menu_recuso, dados

def isDate(data_user, user):
    try:
        data_ = str(data_user).split("/")

        dia = int(data_[0])
        mes = int(data_[1])
        ano = int(data_[2])

        newDate = datetime.date(ano, mes, dia)
        data_limite = datetime.date.today() + datetime.timedelta(days=7)

        if newDate >= datetime.date.today():
            if newDate <= data_limite:

                finalDate = str(newDate).split("-")
                finalDate= f"{finalDate[2]}-{finalDate[1]}-{finalDate[0]}"
                writeText(user, "data", finalDate)

                return True, '' #é uma data valida

            else:

                return False, 6 #é uma data, é maior que dois dias

        else:

            return False, 7 #data anterior a hoje
        
    except Exception:

        return False, 8 #não é uma data


