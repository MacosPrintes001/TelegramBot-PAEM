from datetime import date, datetime, timedelta
import datetime
import json
from logging import ERROR, error
import requests
import telebot
from telebot.apihelper import send_message
import dados_bot
import conexao_bot as conect

token = dados_bot.btoken

bot = telebot.TeleBot(token, threaded=True)


class Alunos():
    def __init__(self):
        self.para_si = None
        self.data = None
        self.hora_inicio = None
        self.hora_fim = None
        self.nome = None
        self.telefone = None
        self.campus = None
        self.cpf = None
        self.matricula= None
        self.recurso = None
        self.id_discente = None
        self.id_usuario = None
        self.id_recurso = None
        

aluno = Alunos()

@bot.message_handler(commands=['start'])
def inicio(message):
    chat_id = message.chat.id
    bot.reply_to(message, "Olá, sou o Bot de agendamento da UFOPA, para fazer uma socitação de acesso,"
                          " basta enviar os seguintes dados NA ORDEM PEDIDA:\n\n"
                          "A solicitação de agendamento é para você?\n"
                          "CPF\n"
                          "Nº da Matricula\n"
                          "data que quer agendar\n"
                          "Horario requerido\n"
                          "Local desejado\n"
                          "Nº do seu telefone")

    e = bot.send_message(chat_id, "Ex:\nSim\n030.511.070-32\n2019004525\n24/08/2022\n08:00 as 10:00\nBiblioteca\n"
                                  "(93)992991452560")

    bot.register_next_step_handler(e, check_dados)


def check_dados(message):

    usuario = message.from_user.id
    chat_id = message.chat.id
    mensagem = str(message.text)
    bot.send_message(chat_id, "Certo, aguarde um momento enquanto eu confiro os dados...")

    try:
        para_si, cpf, matricula, data, hora, recurso, telefone = mensagem.split('\n')

        print("splitei")

        if para_si is not None and cpf is not None and matricula is not None and \
            data is not None and hora is not None and telefone is not None and recurso is not None: #saber se não há dados vazios
            
            print("entrei if dados não vazios")

            data =str(data)
            para_si = str(para_si)
            cpf = str(cpf)
            matricula = str(matricula) 
            hora = str(hora) 
            recurso = str(recurso) 
            telefone = str(telefone)

            print("tranformei tudo em string")

            dv = data_valida(data) #verificação data valida

            if dv == True:
                print("entrei if data valida")
                try:
                    print("tentei conexão")
                    resp, nome, id_discente, campus, id_recurso, id_usuario, token = conect.login(cpf, matricula, recurso)
                    print("recebi dados")

                    if resp:
                        print("resp não foi nula")
                        prepara_agendar(para_si, campus, cpf, matricula, data, hora, recurso,\
                                telefone,nome, id_discente, id_usuario,id_recurso, token, usuario)
                        
                    else:

                        print("ERRO DE CONEXÃO")

                        bot.send_message(chat_id, "Houve algum erro no servidor, verifique se você enviou o cpf ou matricula certos pois eu preciso que você envie tudo corretamente, igual ao "
                                                    "indicado, Digite SIM para tentar novamente, ou NÂO para encerrar o acesso.")
                except Exception:
                    print("ERRO SERVIDOR")
                    bot.send_message(chat_id, "Houve um erro no servidor digite /start e tente novamente, e não esqueça de verificar se os dados estão corretos")

            else:
                print("DATA INVALIDA")
                bot.send_message(chat_id, "Parece que a data que você passou não é valida, tente "
                                          "novamente com uma data valida. Basta clicar em /start para tentar de novo")
        
        else:
            print("FALTA DE DADOS")
            bot.send_message(chat_id, "Olha parece que faltaram alguns dados, envie /start e tente de novo")

    except Exception:
        print(Exception)
        print("ERRO CHECK DADOS")
        bot.send_message(chat_id, "Houve um erro, verifique se você enviou todos os dados de forma correta")
        bot.send_message(chat_id, "Precione /start e tente novamente")



def prepara_agendar(para_si, campus, cpf, matricula, data, hora, 
recurso, telefone,nome, id_discente, id_usuario, id_recurso, token, chat_id): #Fazendo ultimas verificações e criando classe aluno
    bot.send_message(chat_id, f"Falta pouco, tenha paciencia....")
    erro = False
    try:
        try:
            hora_inicio, _ , hora_fim = str(hora).split()
            if hora_inicio is not None and hora_fim is not None:
                setattr(aluno, 'hora_inicio', hora_inicio)
                setattr(aluno, 'hora_fim', hora_fim)
        except Exception:
            erro = True
            bot.send_message(chat_id, "Deu erro no horario solicitado, clique em /start e tente novamente")

        try:
            data = str(data).replace("/", "-")
            setattr(aluno, 'data', data)
        except EOFError:
            erro = True            
            bot.send_message(chat_id, "Houve um erro com a data informada, a data deve ser enviada com a barra / como separador e o ano não deve ser encurtado digite /start e tente novamente")
        
        if str(para_si).lower() == "sim":
            setattr(aluno, 'para_si', 1)
        elif str(para_si).lower() == "não":
            setattr(aluno, 'para_si', -1)   
        else:
            bot.send_message(chat_id, "Não entendi se o atendimento é para você, clique em /start e tente denovo")
            erro = True

        if erro is False:
            setattr(aluno,'campus', campus)
            setattr(aluno, 'matricula', matricula)
            setattr(aluno, 'nome', nome)
            setattr(aluno, 'cpf', cpf)
            setattr(aluno, 'id_discente', id_discente)
            setattr(aluno, 'id_usuario', id_usuario)
            setattr(aluno, 'telefone', telefone)
            setattr(aluno, 'recurso', recurso)
            setattr(aluno, 'id_recurso', id_recurso)

            dados_aluno = {"para_si": int(aluno.para_si),
                            "data": aluno.data,
                            "hora_inicio": f"{aluno.hora_inicio}:00",
                            "hora_fim": f"{aluno.hora_fim}:00",
                            "status_acesso": 1,
                            "nome": aluno.nome,
                            "fone": aluno.telefone,
                            "cpf": aluno.cpf,
                            "usuario_id_usuario": int(aluno.id_usuario),
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
        bot.send_message(chat_id, "ERRO NO METODO")
    

def data_valida(data_user):  # validando a data enviada
    try:
        resp = ""
        data_ = str(data_user).split("/")

        dia = int(data_[0])
        mes = int(data_[1])
        ano = int(data_[2])

        newDate = datetime.date(ano, mes, dia)
        print(type(date.today()))

        data_limite = date.today() + timedelta(days=2)

        if newDate >= date.today() and newDate <= data_limite:
            resp = True
        else:
            resp = False
        
        return resp

    except Exception:
        print("deu merda")


@bot.message_handler(func=lambda m : True )
def indef(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Desculpe não entendi o que disse, clique em /start para fazer uma solicitação de acesso")


try:
    bot.polling(none_stop=True, interval=5, timeout=20)
except:
    bot.polling(none_stop=True, interval=5, timeout=20)
