import dados_bot
import telebot
from random import randint
import conection as cnt
import botUtil

token = dados_bot.agendamentoBotToken
bot = telebot.TeleBot(token)

arc = ""


@bot.message_handler(commands=['start']) #INICIANDO O BOT
def start(message):
    usuario = str(message.from_user.id)
    botUtil.removeFile(usuario)
    chat_id = message.chat.id
    r = bot.send_message(chat_id,
                         "Olá, bem-vindo(a) ao sistema de agendamento da UFOPA. Você já possui cadastro no sistema?\n1 - Sim\n2 - Não")
    bot.register_next_step_handler(r, registrado)


@bot.message_handler(commands=['stop'])
def stop(message):
    bot.reply_to(message, "Certo, quando quiser realizar uma solicitação basta me chamar que estarei aqui")
    bot.send_message(message.chat.id, "Serviço encerrado")


def registrado(message):
    try:
        chat_id = message.chat.id
        msg = str(message.text).lower().strip()

        if msg == "/stop":
            stop(message)

        elif int(msg) == 1:
            #requestCPF(message)  #INICIO ATENDIMENTO
            print("Tentativa de login")

        elif int(msg) == 2: #USUARIO NÃO POSSUI CADASTRO O SISTEMA
            link = "http://www.minhavidaacademica.com.br/View/discente/cadastrar_disc.php"
            bot.send_message(chat_id,
                             f"Certo, vá no link abaixo, faça seu cadastro e depois volte aqui comigo.\n{link}")
        
        else: #USUARIO NÃO ENVIOU UMA OPÇÃO VALIDA
            r = bot.send_message(chat_id, "Não entendi o que você disse. Você já possui cadastro?\n1 - Sim\n2 - Não")
            bot.register_next_step_handler(r, registrado)

    except Exception: #USUARIO ENVIOU UM CARACTER NÃO RECONHECIDO
        r = bot.send_message(message.chat.id, "Não entendi o que você disse. Você já possui cadastro?\n1 - Sim\n2 - Não")
        bot.register_next_step_handler(r, registrado)

try:
    bot.polling(none_stop=True, interval=5, timeout=20)
except:
    bot.polling(none_stop=True, interval=5, timeout=20)
