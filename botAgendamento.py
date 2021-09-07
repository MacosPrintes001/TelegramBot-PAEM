<<<<<<< Updated upstream
from botMain import registrado
=======
>>>>>>> Stashed changes
import dados_bot
import telebot

token = dados_bot.agendamentoBotToken

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Olá, bem-vindo(a) ao sistema de agendamento da UFOPA. Você já possui cadastro no sistema?")
    r = bot.send_message(chat_id, "1 - Sim\n2- Não")
    bot.register_next_step_handler(r, registrado)


def registrado(message):
    try:
        chat_id = message.chat.id
        resp = int(message.text)
        if resp == 1:
            pass #começa atendimento
        elif resp == 2:
            bot.send_message(chat_id, "Certo, vá com o meu amigo @UFOPA_BOT e faça seu cadastro com ele e depois volte aqui comigo")
        else:
            bot.send_message(chat_id, "Não entendi o que você disse. Você já possui cadastro?")
            r = bot.send_message(chat_id, "1 - Sim\n2- Não")
            bot.register_next_step_handler(r, registrado)   

    except Exception:
        bot.send_message(message.chat.id, "Responda com NÚMERO da sua opção")
        r = bot.send_message(chat_id, "1 - Sim\n2 - Não")
        bot.register_next_step_handler(r, registrado)




try:
    bot.polling(none_stop=True, interval=5, timeout=20)
except:
    bot.polling(none_stop=True, interval=5, timeout=20)