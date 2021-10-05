from datetime import date, datetime, timedelta
import datetime
import conection


arc = ""

def isTime(time, user): #Se preciar de tempo maior é só dividir horaIni e horaFim e verificar se algum esta em horarios

    horaios = {'08:00 as 10:00','10:00 as 12:00', '14:00 as 16:00', 
                '16:00 as 18:00', '18:00 as 20:00', '20:00 as 22:00'}
    if time in horaios:

        horaIni, _, horaFim = str(time).split(" ")


        arc = open(user+".txt", "a")
        arc.write(f"HORA_INI: {horaIni}\n")
        arc.write(F"HORA_FIM: {horaFim}\n")
        arc.close()

        protocol = conection.getProtocol()
        conection.backupDados(protocol, horaIni)
        conection.backupDados(protocol, horaFim)
        return True
    else:
        return False


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

                arc = open(user+".txt", "a")
                finalDate = str(newDate)
                arc.write(f"DATA: {finalDate}\n")
                arc.close()

                return True, '' #é uma data valida

            else:
                return False, 6 #é uma data, é maior que dois dias

        else:
            return False, 7 #data anterior a hoje
        
    except Exception:
        print("ERRO Data")
        return False, 8 #não é uma data


