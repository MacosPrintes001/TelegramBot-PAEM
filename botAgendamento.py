import re
from typing import Annotated
from time import sleep
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
            pedeCPF(message) #começa atendimento
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


def pedeCPF(message):
    try:
        chat_id = message.chat.id
        protocolo = str(message.from_user.id + random.random()).replace(".", "") #criei protocolo com o idUsuario do telegram e um numero aletorio
        
        #enviar protocolo pro banco
        cnt.backupDados("NULL", protocolo)

        r = bot.send_message(chat_id, "Certo, pra começar vou precisar do seu CPF. ENVIE APENAS OS NÚMEROS")
        bot.register_next_step_handler(r, fazLogin)

    except:
        pass


def fazLogin(message):
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
            bot.register_next_step_handler(m, buscaDados)

        else:
            if errorCode == 0:
                m = bot.send_message(chat_id, "Erro no servidor, tente novamente. Envie seu cpf depois sua matricula")
                bot.register_next_step_handler(m, fazLogin)

            elif errorCode == 1:
                bot.send_message(chat_id, "Eu não achei esse cpf no servidor, caso não tenha uma conta ainda basta falar com meu amigo @UFOPA_BOT e criar uma conta.")
                msg = bot.send_message(chat_id, "Caso você já possua uma conta, revise seus dados e mande novamente")
                bot.register_next_step_handler(msg, fazLogin)
            else:
                msg = bot.send_message(chat_id, "Houve um erro desconhecido. Tente novamente")
                bot.register_next_step_handler(msg, fazLogin)

    except Exception:
        bot.send_message(chat_id, "Olha, parece que você digitou algo de errado. Tente novamente, e lembre-se são apenas os NÚMEROS  do cpf")
        r = bot.send_message(chat_id, "Exemplo: 03051103072")
        bot.register_next_step_handler(r, fazLogin)



def buscaDados(message):

    matricula = str(message.text)
    chat_id = message.chat.id

    resp, errorCode = cnt.dadosUsuario(matricula)
    if resp:

            m = bot.send_message(chat_id, f"Tudo certo, login efetuado, agora vou precisar da sua matricula")
            bot.register_next_step_handler(m, buscaDados)

    else:
        if errorCode == 3:
            m = bot.send_message(chat_id, "Erro no servidor, tente novamente. Envie seu cpf depois sua matricula")
            bot.register_next_step_handler(m, fazLogin)

        elif errorCode == 2:
            bot.send_message(chat_id, "Eu não achei esses dados no servidor, caso não tenha uma conta ainda basta falar com meu amigo @UFOPA_BOT e criar uma conta.")
            msg = bot.send_message(chat_id, "Caso você já possua uma conta, revise seus dados e mande novamente")
            bot.register_next_step_handler(msg, fazLogin)
        else:
            msg = bot.send_message(chat_id, "Houve um erro desconhecido. Tente novamente")
            bot.register_next_step_handler(msg, fazLogin)

    

@bot.message_handler(func=lambda m : True )
def indef(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Desculpe, não entendi o que disse, por favor clique em /start para iniciar o atendimento")


try:
    bot.polling(none_stop=True, interval=5, timeout=20)
except:
    bot.polling(none_stop=True, interval=5, timeout=20)