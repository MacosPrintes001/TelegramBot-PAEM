import telebot
import dados_bot


token = dados_bot.mainBotToken
bot = telebot.TeleBot(token=token)

@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    nome = f"{message.from_user.first_name}"

    bot.send_message(chat_id, f"Olá {nome} sejá bem vindo ao sistema virtual da UFOPA. Para acessar as proximas etapas você precisa estar cadastrado(a) no sistema \
                                me diga, você já esta cadastrado(a)?")
    r = bot.send_message(chat_id, "1 - Sim\n2 - Não")
    bot.register_next_step_handler(r, registrado)
#função registrar usuario


def registrado(message):
    try:
        chat_id = message.chat.id
        resp = int(message.text)
        link = "http://www.minhavidaacademica.com.br/View/discente/cadastrar_disc.php"
        if resp == 1:
            menu(message)
        elif resp == 2:
            bot.send_message(chat_id, f"Certo, entre no link abaixo, faça seu cadastro e depois volte aqui")
            bot.send_message(chat_id, f"{link}")
        else:
            bot.send_message(chat_id, "Desculpe não entedi o que disse. Você já possui cadastro?")
            r = bot.send_message(chat_id, "1 - Sim\n2 - Não")
            bot.register_next_step_handler(r, registrado)
    except Exception:
        bot.send_message(message.chat.id, "Responda com NÚMERO da sua opção")
        r = bot.send_message(chat_id, "1 - Sim\n2 - Não")
        bot.register_next_step_handler(r, registrado)
            
def menu(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "OK, o que eu posso fazer por você?")
    m = bot.send_message(chat_id, "1 - Agendamento\n2 - Requisição de Atestado de Matrícula\n3 - Abono de Faltas")
    bot.register_next_step_handler(m, encaminhaBot)


def encaminhaBot(message):
    chat_id = message.chat.id

    opc = int(message.text)
    try:
        opc = int(opc)
        if opc == 1:
            bot.send_message(chat_id, "OK, basta você falar com meu amigo @UfopaAgendamentoBot para agendar um horario")        

        else:
            bot.send_message(chat_id, "Esta função ainda não foi implementada, escolha outra")
            menu(message)
    except Exception:
        bot.send_message(chat_id, "Por favor selecione o NÚMERO da opção desejada")
        menu(message)



@bot.message_handler(func=lambda m : True )
def indef(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Desculpe, não entendi o que disse, por favor clique em /start para iniciar o atendimento")

try:
    bot.polling(none_stop=True, interval=5, timeout=20)
except:
    bot.polling(none_stop=True, interval=5, timeout=20)