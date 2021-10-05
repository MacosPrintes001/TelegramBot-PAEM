from datetime import datetime
from typing import Container
from telebot.types import Update
import dados_bot
import telebot
from random import randint
import conection as cnt
import botUtil

token = dados_bot.agendamentoBotToken

bot = telebot.TeleBot(token)

arc = ""


@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    r = bot.send_message(chat_id,
                         "Olá, bem-vindo(a) ao sistema de agendamento da UFOPA. Você já possui cadastro no sistema?\n1 - Sim\n2 - Não")
    bot.register_next_step_handler(r, registrado)


def registrado(message):
    try:
        chat_id = message.chat.id
        resp = int(message.text)

        if resp == 1:
            requestCPF(message)  # começa atendimento

        elif resp == 2:

            bot.send_message(chat_id,
                             "Certo, vá com o meu amigo @UFOPA_BOT e faça seu cadastro com ele e depois volte aqui comigo")

        else:
            r = bot.send_message(chat_id, "Não entendi o que você disse. Você já possui cadastro?\n1 - Sim\n2 - Não")
            bot.register_next_step_handler(r, registrado)

    except Exception:
        r = bot.send_message(message.chat.id, "Responda com NÚMERO da sua opção.\n1 - Sim\n2 - Não")
        bot.register_next_step_handler(r, registrado)


def requestCPF(message):
    try:
        chat_id = message.chat.id
        r = bot.send_message(chat_id, "Certo, pra começar vou precisar do seu CPF.\nENVIE APENAS OS NÚMEROS")
        bot.register_next_step_handler(r, doLogin)

    except:
        pass


def doLogin(message):
    try:
        chat_id = message.chat.id
        msg = str(message.text)
        user = str(message.from_user.id)

        cpf = f'{msg[:3]}.{msg[3:6]}.{msg[6:9]}-{msg[9:]}'

        bot.send_message(chat_id, "Ok, só um segundo enquanto eu tento fazer seu login")

        # indo no banco pegar os dados
        resp, errorCode = cnt.login(cpf, user)

        if resp:

            m = bot.send_message(chat_id, f"Tudo certo, login efetuado, agora vou precisar da sua matricula")
            bot.register_next_step_handler(m, searchUserData)

        else:
            if errorCode == 0:
                m = bot.send_message(chat_id, "Erro no servidor, tente novamente. Envie seu cpf depois sua matricula")
                bot.register_next_step_handler(m, doLogin)

            elif errorCode == 1:
                bot.send_message(chat_id,
                                 "Eu não achei esse cpf no servidor, caso não tenha uma conta ainda basta falar com meu amigo @UFOPA_BOT e criar uma conta.")
                msg = bot.send_message(chat_id, "Caso você já possua uma conta, revise seus dados e mande novamente")
                bot.register_next_step_handler(msg, doLogin)
            else:
                msg = bot.send_message(chat_id, "Houve um erro desconhecido. Tente novamente")
                bot.register_next_step_handler(msg, doLogin)

    except Exception:
        bot.send_message(chat_id,
                         "Olha, parece que você digitou algo de errado. Tente novamente, e lembre-se são apenas os NÚMEROS  do cpf")
        r = bot.send_message(chat_id, "Exemplo: 03051103072")
        bot.register_next_step_handler(r, doLogin)


def searchUserData(message):
    try:

        matricula = str(message.text)
        print(matricula)
        chat_id = message.chat.id
        user = str(message.from_user.id)

        resp, info, recursos_campus = cnt.dadosUsuario(matricula, user)
        if resp:

            # menu = botUtil.makeMenu(recursos_campus)

            bot.send_message(chat_id, f"Matricula Valida. Qual recurso vecê gostaria de reservar?")
            m = bot.send_message(chat_id, f"{recursos_campus}")
            bot.register_next_step_handler(m, requestHour)

        else:
            if info == 3:
                m = bot.send_message(chat_id, "Erro no servidor, tente novamente. Envie sua matricula")
                bot.register_next_step_handler(m, searchUserData)

            elif info == 2:
                m = bot.send_message(chat_id, "Não achei essa matricula. Tente novamente")
                bot.register_next_step_handler(m, searchUserData)
    except Exception:
        pass


# VARIAVEL GLOBAL
horario = ''


def requestHour(message):
    global horario
    chat_id = message.chat.id
    id_recurso = int(message.text)
    user = str(message.from_user.id)

    resp, errorCode, menu = cnt.verific_id(id_recurso)

    if resp:
        arc = open(user + ".txt", "a")
        arc.write(f"ID_RECURSO: {id_recurso}\n")
        arc.close()

        menuHour, hora = cnt.getHora(id_recurso)

        # ATRIBUI À VARIAVEL GLOBAL O DICIONARIO COM AS HORAS
        horario = hora

        r = bot.send_message(chat_id, f"Escolha a opção referente aos horarios abaixo.\n{menuHour}")

        bot.register_next_step_handler(r, procHour)

    else:

        if errorCode == 4:  # id não encontrado
            bot.send_message(chat_id, "Opção não reconhecida, tente novamente")
            r = bot.send_message(chat_id, f"{menu}")
            bot.register_next_step_handler(r, requestHour)

        elif errorCode == 5:  # algo que não é um id
            m = bot.send_message(chat_id, f"Houve um erro no servidor, tente novamente.\n{menu}")
            bot.register_next_step_handler(m, requestHour)


def procHour(message):
    # RETORNA AS HORAS REFERENTE A OPÇÃO ESCOLHIDA
    try:
        x = horario[int(message.text)]
        chat_id = message.chat.id
        user = str(message.from_user.id)

        resp = botUtil.isTime(x, user)

        if resp:
            bot.send_message(chat_id, "Tudo certo, Hora valida. Mande a data para a qual vai ser a reserva.")
            r = bot.send_message(chat_id, "Mande a data no seguinte formato dd/mm/yyyy")
            bot.register_next_step_handler(r, procDate)

    except Exception:
        chat = message.chat.id
        r = bot.send_message(chat, "Horario inválido. Tente novamente")
        bot.register_next_step_handler(r, procHour)


def procDate(message):
    data_user = str(message.text)
    user = str(message.from_user.id)
    chat_id = message.chat.id
    resp, errorCode = botUtil.isDate(data_user, user)

    if resp:
        r = bot.send_message(chat_id, f"Data valida. A reserva é para você?\n1 - Sim\n2 - Não")
        bot.register_next_step_handler(r, forYou)

    else:
        if errorCode == 6:
            r = bot.send_message(chat_id, "Data inválida. A data não pode ser posterior a dois dias")
            bot.register_next_step_handler(r, procDate)

        elif errorCode == 7:
            r = bot.send_message(chat_id,
                                 "Data inválida. A data não pode ser anterior ao dia de hoje, tente novamente.")
            bot.register_next_step_handler(r, procDate)

        else:
            bot.send_message(chat_id, "Formato de data invalido. Envie novamente, siga o exemplo")
            r = bot.send_message(chat_id, "Ex: 24/10/2021")
            bot.register_next_step_handler(r, procDate)


def forYou(message):
    try:
        chat_id = message.chat.id
        msg = int(message.text)
        user = str(message.from_user.id)

        if msg == 1:

            arc = open(user + ".txt", "a")
            arc.write(f"PARA_SI: 1\n")
            arc.close()

            r = bot.send_message(chat_id,
                                 "Ok, ultima coisa, por questões de segurança o Telegram não me permite  ver seu numero de telelfone, então vou precisar qeu você mande ele pra mim")
            bot.register_next_step_handler(r, PhoneNumber)

        elif msg == 2:

            arc = open(user + ".txt", "a")
            arc.write(f"PARA_SI: 2\n")
            arc.close()

            r = bot.send_message(chat_id,
                                 "Ok, ultima coisa, por questões de segurança o Telegram não me permite  ver seu numero de telelfone, então vou precisar qeu você mande ele pra mim")
            bot.register_next_step_handler(r, PhoneNumber)

        else:
            r = bot.send_message(chat_id, "Não entendi, essa reserva é para você?\n1 - Sim\n2 - Não")
            bot.register_next_step_handler(r, forYou)

    except Exception:
        chat = message.chat.id
        r = bot.send_message(chat, "Não entendi, essa reserva é para você?\n1 - Sim\n2 - Não")
        bot.register_next_step_handler(r, forYou)


def PhoneNumber(message):
    user = str(message.from_user.id)
    phone = str(message.text)
    arc = open(user + ".txt", "a")
    arc.write(f"TELEFONE: {phone}\n")
    arc.close()
    callReservation(message)


def callReservation(message):
    chat_id = message.chat.id

    # pegar dados e fazer reserva
    user = str(message.from_user.id)
    cnt.makeReservation(user)

    n = randint()
    print(n)
    protocolo = message.from_user.id + n

    bot.send_message(chat_id, "Ok, só um segundo enquanto eu faço sua reserva")
    bot.send_message(chat_id, f"Tudo certo, reserva feita com sucesso, seu protocolo é {protocolo}")

    # DELETAR ARQUIVOS TXT


@bot.message_handler(func=lambda m: True)
def indef(message):
    chat_id = message.chat.id
    bot.send_message(chat_id,
                     "Desculpe, não entendi o que disse, por favor clique em /start para iniciar o atendimento")


try:
    bot.polling(none_stop=True, interval=5, timeout=20)
except:
    bot.polling(none_stop=True, interval=5, timeout=20)
