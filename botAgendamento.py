import dados_bot
import telebot

token = dados_bot.agendamentoBotToken

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start(message):
    id = message.chat.id
    bot.send_message(id, "Olá, bom dia")

try:
    bot.polling(none_stop=True, interval=5, timeout=20)
except:
    bot.polling(none_stop=True, interval=5, timeout=20)