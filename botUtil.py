from datetime import date, datetime, timedelta
import datetime
import conection



def isTime(time): #Se preciar de tempo maior é só dividir horaIni e horaFim e verificar se algum esta em horarios

    horaios = {'08:00 as 10:00','10:00 as 12:00', '14:00 as 16:00', 
                '16:00 as 18:00', '18:00 as 20:00', '20:00 as 22:00'}
    print(time, type(time))
    if time in horaios:

        horaIni, _, horaFim = str(time).split(" ")
        protocol = conection.getProtocol()
        conection.backupDados(protocol, horaIni)
        conection.backupDados(protocol, horaFim)
        return True
    else:
        return False


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

                protocol = conection.getProtocol()
                conection.backupDados(protocol, str(data_user))
                return True, '' #é uma data valida

            else:
                return False, 6 #é uma data, é maior que dois dias

        else:
            return False, 7 #data anterior a hoje
        
    except Exception:
        return False, 8 #não é uma data


