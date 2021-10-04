from datetime import datetime
from typing import Container
from telebot import handler_backends
from telebot.types import Update
import dados_bot
import telebot
import random
import conection as cnt
import botUtil

token = dados_bot.agendamentoBotToken

bot = telebot.TeleBot(token)

arc = ""
tagUser = "USER: "
tagBot = "\t BOT: "


@bot.message_handler(commands=['start'])
def start(message):  

    chat_id = message.chat.id
    text = str(message.text)
    r = bot.send_message(chat_id, "Olá, bem-vindo(a) ao sistema de agendamento da UFOPA. Você já possui cadastro no sistema?\n1 - Sim\n2 - Não")
    
    """
    user = str(message.from_user.id)
    arc = open(user+".txt", "w")
    arc.write(f"{tagUser} {text}\n")
    arc.write(f"{tagBot} {str(r.text)}\n")"""
    
    bot.register_next_step_handler(r, registrado)


def registrado(message):
    try:
        
        """t = str(message.text)
        user = str(message.from_user.id)
        arc = open(user+".txt", "a")
        arc.write(f"{tagUser} {t}\n")"""

        chat_id = message.chat.id
        resp = int(message.text)

        if resp == 1:
            requestCPF(message) #começa atendimento

        elif resp == 2:

            arc.write(f"{tagUser} 2\n")
            arc.write(f"{tagBot} Certo, vá com o meu amigo @UFOPA_BOT e faça seu cadastro com ele e depois volte aqui comigo")

            bot.send_message(chat_id, "Certo, vá com o meu amigo @UFOPA_BOT e faça seu cadastro com ele e depois volte aqui comigo")
            
        else:
            r = bot.send_message(chat_id, "Não entendi o que você disse. Você já possui cadastro?\n1 - Sim\n2 - Não")
            bot.register_next_step_handler(r, registrado)   

    except  Exception:
        r = bot.send_message(message.chat.id, "Responda com NÚMERO da sua opção.\n1 - Sim\n2 - Não")
        bot.register_next_step_handler(r, registrado)


def requestCPF(message):
    try:
        user = str(message.from_user.id)
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
        
        #print(cpf) 

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
        
        menu = botUtil.makeMenu(recursos_campus)

        
        
        bot.send_message(chat_id, f"Matricula Valida. Qual recurso vecê gostaria de reservar?")
        
        m = bot.send_message(chat_id, f"{menu}")

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

        menuHour, id_chat, id_recursoUser = cnt.getHora(id_recurso, chat_id)
        
        bot.send_message(id_chat, f"Escolha um destes horaios abaixo.\n{menuHour}")
        r = bot.send_message(chat_id, "É para mandar um texto com o horario.\nex: 08:00 as 10:00")
        bot.register_next_step_handler(r, procHour)
        
    else:
        
        if errorCode == 4: #id não encontrado
            bot.send_message(chat_id, "Opção não reconhecida, tente novamente")
            r = bot.send_message(chat_id, f"{menu}")
            bot.register_next_step_handler(r, requestHour)

        elif errorCode == 5: #algo que não é um id
            m = bot.send_message(chat_id, f"Houve um erro no servidor, tente novamente.\n{menu}")
            bot.register_next_step_handler(m, requestHour)


def procHour(message):
    chat_id = message.chat.id
    msg = str(message.text)
    resp = botUtil.isTime(msg)

    id_rec = bot.get_updates()[-1].message.text
    print(id_rec)

    if resp:
        protocol = cnt.getProtocol()
        cnt.backupDados(protocol, msg)

        bot.send_message(chat_id, "Tudo certo, Hora valida. Mande a data para a qual vai ser a reserva.")
        r = bot.send_message(chat_id, "Mande a data no seguinte formato dd/mm/yyyy")
        bot.register_next_step_handler(r, procDate)

    else:
        r = bot.send_message(chat_id, "Horario inválido. Tene novamente")
        bot.register_next_step_handler(r, procHour)



def procDate(message):
    data_user = str(message.text)
    chat_id = message.chat.id
    resp, errorCode = botUtil.isDate(data_user)

    if resp:
        r = bot.send_message(chat_id, f"Data valida. A reserva é para você?\n1 - Sim\n2 - Não")
        bot.register_next_step_handler(r, forYou)

    else:
        if errorCode == 6:
            r = bot.send_message(chat_id, "Data inválida. A data não pode ser posterior a dois dias")
            bot.register_next_step_handler(r, procDate)
        
        elif errorCode == 7:
            r = bot.send_message(chat_id, "Data inválida. A data não pode ser anterior ao dia de hoje, tente novamente.")
            bot.register_next_step_handler(r, procDate)

        else:
            bot.send_message(chat_id, "Formato de data invalido. Envie novamente, siga o exemplo")
            r = bot.send_message(chat_id, "Ex: 24/10/2021")
            bot.register_next_step_handler(r, procDate)



def forYou(message):
    chat_id = message.chat.id
    msg = int(message.text)

    if msg == 1:
        para_si = 1

        protocol = cnt.getProtocol()
        cnt.backupDados(protocol, para_si)

        r = bot.send_message(chat_id, "Ok, ultima coisa, por questões de segurança o Telegram não me permite  ver seu numero de telelfone, \
                                     então vou precisar qeu você mande ele pra mim")
        bot.register_next_step_handler(r, PhoneNumber)

    elif msg == 2:
        para_si = -1
        protocol = cnt.getProtocol()
        cnt.backupDados(protocol, para_si)
        r = bot.send_message(chat_id, "Ok, ultima coisa, por questões de segurança o Telegram não me permite  ver seu numero de telelfone, então vou precisar qeu você mande ele pra mim")
        bot.register_next_step_handler(r, PhoneNumber)

    else:
        r = bot.send_message(chat_id, "Não entendi, essa reserva é para você?\n1 - Sim\n2 - Não")
        bot.register_next_step_handler(r, forYou)


def PhoneNumber(message):
    msg = message.text
    chat_id = message.chat.id
    r = bot .send_message(chat_id, f"Seu numero é {msg}, isso está correto?\n1 - Sim\n2 - Não")
    bot.register_next_step_handler(r, respPhone)


def respPhone(message):
    resp = int(message.text)
    chat_id = message.chat.id

    if resp == 1:
        protocol = cnt.getProtocol()
        cnt.backupDados(protocol, resp) #Numero de telefone

        bot.send_message(chat_id, "Ok, só um segundo enquanto eu faço sua reserva")
        bot.send_message(chat_id, f"Tudo certo, reserva feita com sucesso, seu protocolo é {protocol}")

        '''resp = cnt.makeReservation()

        if resp == 'OK':

        else:
            bot.send_message(chat_id, f"Reserva malsucedida, seu protocolo é {protocol}")'''
    else:
        r = bot.send_message(chat_id, "Certo, digite seu telefone novamente.")
        bot.register_next_step_handler(r, PhoneNumber)



@bot.message_handler(func=lambda m : True )
def indef(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Desculpe, não entendi o que disse, por favor clique em /start para iniciar o atendimento")

try:
    bot.polling(none_stop=True, interval=5, timeout=20)
except:
    bot.polling(none_stop=True, interval=5, timeout=20)