from telebot import *
# import logic
from logic import *
TOKEN = 'token'


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


def main():
    bot.infinity_polling(True)
main()
