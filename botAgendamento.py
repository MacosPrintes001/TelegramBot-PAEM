from telebot.types import Update
import dados_bot
import telebot
import random
import conection as cnt


token = dados_bot.agendamentoBotToken

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Olá, bem-vindo(a) ao sistema de agendamento da UFOPA. Você já possui cadastro no sistema?")
    r = bot.send_message(chat_id, "1 - Sim\n2 - Não")
    bot.register_next_step_handler(r, registrado)

def registrado(message):
    try:
        chat_id = message.chat.id
        resp = int(message.text)
        if resp == 1:
            requestCPF(message) #começa atendimento
        elif resp == 2:
            bot.send_message(chat_id, "Certo, vá com o meu amigo @UFOPA_BOT e faça seu cadastro com ele e depois volte aqui comigo")
        else:
            bot.send_message(chat_id, "Não entendi o que você disse. Você já possui cadastro?")
            r = bot.send_message(chat_id, "1 - Sim\n2 - Não")
            bot.register_next_step_handler(r, registrado)   

    except Exception:
        bot.send_message(message.chat.id, "Responda com NÚMERO da sua opção")
        r = bot.send_message(chat_id, "1 - Sim\n2 - Não")
        bot.register_next_step_handler(r, registrado)


def requestCPF(message):
    try:
        chat_id = message.chat.id
        protocol = str(message.from_user.id + random.random()).replace(".", "") #criei protocolo com o idUsuario do telegram e um numero aletorio
        #enviar protocolo pro banco
        #cnt.backupDados("NULL", protocolo)
        r = bot.send_message(chat_id, "Certo, pra começar vou precisar do seu CPF.\nENVIE APENAS OS NÚMEROS")
        bot.register_next_step_handler(r, doLogin)

    except:
        pass


def doLogin(message):
    try:
        chat_id = message.chat.id
        msg = str(message.text)

        cpf = f'{msg[:3]}.{msg[3:6]}.{msg[6:9]}-{msg[9:]}'
        print(cpf) 

        bot.send_message(chat_id, "Ok, só um segundo enquanto eu tento fazer seu login")
        
        #indo no banco pegar os dados
        resp, errorCode = cnt.login(cpf)

        if resp:

            m = bot.send_message(chat_id, f"Tudo certo, login efetuado, agora vou precisar da sua matricula")
            bot.register_next_step_handler(m, searchUserData)

        else:
            if errorCode == 0:
                m = bot.send_message(chat_id, "Erro no servidor, tente novamente. Envie seu cpf depois sua matricula")
                bot.register_next_step_handler(m, doLogin)

            elif errorCode == 1:
                bot.send_message(chat_id, "Eu não achei esse cpf no servidor, caso não tenha uma conta ainda basta falar com meu amigo @UFOPA_BOT e criar uma conta.")
                msg = bot.send_message(chat_id, "Caso você já possua uma conta, revise seus dados e mande novamente")
                bot.register_next_step_handler(msg, doLogin)
            else:
                msg = bot.send_message(chat_id, "Houve um erro desconhecido. Tente novamente")
                bot.register_next_step_handler(msg, doLogin)

    except Exception:
        bot.send_message(chat_id, "Olha, parece que você digitou algo de errado. Tente novamente, e lembre-se são apenas os NÚMEROS  do cpf")
        r = bot.send_message(chat_id, "Exemplo: 03051103072")
        bot.register_next_step_handler(r, doLogin)



def searchUserData(message):

    matricula = str(message.text)
    print(matricula)
    chat_id = message.chat.id

    resp, errorCode, recursos_campus = cnt.dadosUsuario(matricula)
    if resp:

            msg = "Selecinone o Numero da opção\n"
            for i in recursos_campus:
                msg = f"{msg}\n{str(i['id'])} - {str(i['nome'])}"
            
            bot.send_message(chat_id, f"Matricula Valida. Qual recurso vecê gostaria de reservar?")
            
            m = bot.send_message(chat_id, f"{msg}")
            bot.register_next_step_handler(m, requestHour)

    else:
        if errorCode == 3:
            m = bot.send_message(chat_id, "Erro no servidor, tente novamente. Envie sua matricula")
            bot.register_next_step_handler(m, searchUserData)

        elif errorCode == 2:
            m = bot.send_message(chat_id, "Não achei essa matricula. Tente novamente")
            bot.register_next_step_handler(m, searchUserData)
    



def requestHour(message):
    chat_id = message.chat.id
    id_recurso = int(message.text)
    resp, errorCode, menu = cnt.verific_id(id_recurso)

    if resp:
        
        protocolo = cnt.getProtocol
        cnt.backupDados(protocolo, id_recurso)

        menuHora, ponteiro = cnt.getHora(id_recurso)
        r = bot.send_message(chat_id, f"Ecolha um horario.\n{menuHora}")
        bot.register_next_step_handler(r, procHour)
        print(menuHora)

        
        '''r =  bot.send_message(chat_id, "Selecione um periodo.\n1 - Manhã\n2 - Tarde\n3 - Noite")
        bot.register_next_step_handler(r, procHora1)'''
        
    else:
        
        if errorCode == 4: #id não encontrado
            bot.send_message(chat_id, "Opção não reconhecida, tente novamente")
            r = bot.send_message(chat_id, f"{menu}")
            bot.register_next_step_handler(r, requestHour)

        elif errorCode == 5: #algo que não é um id
            m = bot.send_message(chat_id, f"Houve um erro no servidor, tente novamente.\n{menu}")
            bot.register_next_step_handler(m, requestHour)


def procHour(message):
    print("Ponto 3")
    print(message)


'''
def procHora1(message):

    print(message)

    chat_id = message.chat.id
    opc = int(message.text)

    if opc == 1:
        r = bot.send_message(chat_id, "1 - 08:00 as 10:00\n2 - 10:00 as 12:00")
        bot.register_next_step_handler(r, procHora2)

    elif opc == 2:
        r = bot.send_message(chat_id, "1 - 14:00 as 16:00\n2 - 16:00 as 18:00")
        bot.register_next_step_handler(r, procHora2)

    elif opc == 3:
        r = bot.send_message(chat_id, "1 - 18:00 as 20:00\n2 - 20:00 as 22:00")
        bot.register_next_step_handler(r, procHora2)

    else:
        r = bot.send_message(chat_id, "Não entendi o que disse. Você irá querer em qual Turno?\n1 - Manhã\n2 - Tarde\n3 - Noite")
        bot.register_next_step_handler(r, procHora1)



def procHora2(mesage):
    pass
    protocol = cnt.getProtocol
    id = cnt.getDados(protocol, "id_recurso")
    opc = mesage.text
    chat_id = mesage.chat.id
'''




@bot.message_handler(func=lambda m : True )
def indef(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Desculpe, não entendi o que disse, por favor clique em /start para iniciar o atendimento")

try:
    bot.polling(none_stop=True, interval=5, timeout=20)
except:
    bot.polling(none_stop=True, interval=5, timeout=20)