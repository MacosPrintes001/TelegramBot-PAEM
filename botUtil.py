from datetime import date, datetime, timedelta
import datetime
import conection


arc = ""

def isTime(time, user): #Se preciar de tempo maior é só dividir horaIni e horaFim e verificar se algum esta em horarios

    horaios = {'08:00 as 10:00','10:00 as 12:00', '14:00 as 16:00', 
                '16:00 as 18:00', '18:00 as 20:00', '20:00 as 22:00'}

    if time in horaios:

        horaIni, _, horaFim = str(time).split(" ")

        writeText(user, "hora_ini", horaIni)
        writeText(user, "hora_fim", horaFim)

        return True
    else:
        return False


def writeText(user, key, value):
    arc = open(user+".text", "a")
    arc.write(f"{key}: {value}\n")
    arc.close()


def writeJson(user, key, value):
    user_json = dict()
    user_json[key] = value
    
    with open(user+".json", "a") as user:
        #json.dump(user_json
        pass
            
def makeMenu(recursos_campus):
    msg = "Selecinone o Numero da opção\n"
    for i in recursos_campus:
        msg = f"{msg}\n{str(i['id'])} - {str(i['nome'])}"
    
    return msg


def isDate(data_user, user):
    try:
        data_ = str(data_user).split("/")

        dia = int(data_[0])
        mes = int(data_[1])
        ano = int(data_[2])

        newDate = datetime.date(ano, mes, dia)

        data_limite = date.today() + timedelta(days=2)

        if newDate >= date.today():
            if newDate <= data_limite:

                finalDate = str(newDate)
                writeText(user, "data", finalDate)

                return True, '' #é uma data valida

            else:
                return False, 6 #é uma data, é maior que dois dias

        else:
            return False, 7 #data anterior a hoje
        
    except Exception:
        print("ERRO Data")
        return False, 8 #não é uma data


