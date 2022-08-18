from telebot import TeleBot, types
# import logic
from logic import *
import os
TOKEN = '5548950715:AAHqsdXG3JVeM1-Z1K-yF03Q2KLfk-0hehQ'
PORT = int(os.environ.get('PORT', 5000))

bot = TeleBot(TOKEN,parse_mode='html')

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, text = 'Hi, I can parse any URL for you, simply send it to me. '
                                             'For example: '
                                             '<code>https://search.edadeal.io/api/v2/search?addContent=true&groupByMeta=true&maxShops=0&miniOfferEcomColor=blue&numdoc=5&page=1&text=бананы&useClickdaemon=true&useFallbackQuery=true&useMisspeller=true</code>')

@bot.message_handler()
def message_handler(message: types.Message):
    # валидируем url
    if url_validator(message.text):
        # если url валидный – парсим
        o = urlparse(message.text)

        bot.send_message(message.chat.id, text=f'<b>Schema:</b> <code>{o.scheme}</code>\n'
                                               f'<b>Port:</b> <code>{port(o)}</code>\n'
                                               f'<b>Host:</b> <code>{o.netloc}</code>\n'
                                               f'<b>Path:</b> <code>{o.path}</code>\n'
                                               f'<b>Anchor:</b> <code>{anchor(o)}</code>')

        if split_queries(o) == '':
            bot.send_message(message.chat.id, text='<b>No Queries</b>')
        # если есть квери: выписываем в столбик
        else:
            bot.send_message(message.chat.id, text='<b>Queries</b>:\n')

            for queries in split_queries(o):
                bot.send_message(message.chat.id, text=f'<code>{queries}</code>')
    # если url невалидный – пишем ошибку
    else:
        bot.send_message(message.chat.id, text = 'Not a valid URL, try again')

@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://peaceful-retreat-96342.herokuapp.com/' + TOKEN)
    return "!", 200
if __name__ == "__main__":
    server.run(host="0.0.0.0", port=PORT)
