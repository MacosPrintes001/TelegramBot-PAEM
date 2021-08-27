import telebot
import dados_bot


token = dados_bot.mainBotToken
bot = telebot.TeleBot(token=token)

@bot.message_handler(commands=['start'])
def start(message):
    id_telegram = message.from_user.id
    chat_id = message.chat.id
    nome = f"{message.from_user.first_name} {message.from_user.last_name}"

    #A FAZER: verificar se o discente está registrado no banco

    if True: #se o _discente não vazio  
        bot.send_message(chat_id, f"Olá {nome} sejá bem vindo ao sistema virtual da UFOPA. No menu abaixo selecione o NÚMERO da sua opção")
        menu(message)
        
    else:
        #realizar cadastro do cara
        pass

#função registrar usuario

def menu(message):
    chat_id = message.chat.id
    m = bot.send_message(chat_id, "1 - Agendamento\n2 - Requisição de Atestado de Matrícula\n3 - Abono de Faltas")
    bot.register_next_step_handler(m, encaminhaBot)


def encaminhaBot(message):
    chat_id = message.chat.id
    opc = int(message.text)
    if opc == 1:
        bot.send_message(chat_id, "OK, basta você falar com meu amigo @ufopa_agendamento para realiazar seu agendamento")
    else:
        m = bot.send_message(chat_id, "Esta função ainda não foi implementada, escolha outra")
        bot.register_next_step_handler(m, menu)


@bot.message_handler(func=lambda m : True )
def indef(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Desculpe, não entendi o que disse, por favor clique em /start para iniciar o atendimento")

try:
    bot.polling(none_stop=True, interval=5, timeout=20)
except:
    bot.polling(none_stop=True, interval=5, timeout=20)