import re
from typing import Annotated

from telebot.types import VoiceChatEnded
import dados_bot
import telebot
import random
import conection as cnt
from datetime import date


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
            CPF_Matricula(message) #começa atendimento
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


def CPF_Matricula(message):
    try:
        chat_id = message.chat.id
        protocolo = str(message.from_user.id + random.random()).replace(".", "") #criei protocolo com o idUsuario do telegram e um numero aletorio

        #enviar protocolo pro banco

        bot.send_message(chat_id, "Certo, pra começar vou precisar do seu CPF e da sua matricula. Envie seu CPF seguido da sua matricula, segue abaixo um exemplo")
        r = bot.send_message(chat_id, "030.511.030-72 2019002845")
        bot.register_next_step_handler(r, fazLogin)
    except:
        pass


def fazLogin(message):
    try:
        chat_id = message.chat.id
        cpf, matricula = str(message.text).split(" ")

        cpf = str(cpf)
        matricula = str(matricula)

        bot.send_message(chat_id, "Ok, só um segundo enquanto eu tento fazer seu login")
        
        print("fui atras da pessoa")
        resp, errorCode = cnt.login(cpf, matricula)

        if resp:
            print("Login feito")
            bot.send_message(chat_id, "Tudo certo, login efetuado")
        else:
            print("deu ruim")
            if errorCode == 00:
                print("Erro no servidor")
                m = bot.send_message(chat_id, "Erro no servidor, tente novamente. Envie seu cpf depois sua matricula")
                bot.register_next_step_handler(m, fazLogin)

            elif errorCode == 1:
                print("Dados não encontrados")
                bot.send_message(chat_id, "Eu não achei esses dados no servidor, caso não tenha uma conta ainda basta falar com meu amigo @UFOPA_BOT e criar uma conta.")
                msg = bot.send_message(chat_id, "Caso você já possua uma conta, revise seus dados e mande novamente")
                bot.register_next_step_handler(msg, fazLogin)
            else:
                print("Erro desconhecido")
                msg = bot.send_message(chat_id, "Houve um erro desconhecido. Tente novamente")
                bot.register_next_step_handler(msg, fazLogin)

    except Exception:
        bot.send_message(chat_id, "Olha, acho que você mandou algum dado errado. Tente novamente, e lembre-se dar UM espaço entre o CPF  e Matrícula")
        r = bot.send_message(chat_id, "030.511.030-72 2019002845")
        bot.register_next_step_handler(r, fazLogin)


@bot.message_handler(func=lambda m : True )
def indef(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Desculpe, não entendi o que disse, por favor clique em /start para iniciar o atendimento")


try:
    bot.polling(none_stop=True, interval=5, timeout=20)
except:
    bot.polling(none_stop=True, interval=5, timeout=20)