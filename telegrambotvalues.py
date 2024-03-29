import telebot
from config import keys, TOKEN
from extensions import ConvertionException, APIException

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    bot.send_message(message.chat.id, 'Вас приветсвует ValuesssBot')
    bot.send_message(message.chat.id, f'Вот что я умею:\n /values - доступные валюты\n')
    bot.send_message(message.chat.id, 'Для использования ковертера валют введите сообщение ввиде:<имя валюты, цену которой нужно узнать> <имя валюты, в которой надо узнать цену первой валюты> <количество первой валюты>.')

@bot.message_handler(commands=['help'])
def help(message: telebot.types.Message):
    bot.send_message(message.chat.id, f'Вот что я умею:\n /values - доступные валюты\n')
    bot.send_message(message.chat.id,'Для использования ковертера валют введите сообщение ввиде:<имя валюты, цену которой нужно узнать> <имя валюты, в которой надо узнать цену первой валюты> <количество первой валюты>.')

@bot.message_handler(commands=['values'])
def info(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for value in keys.values():
       text = '\n'.join((text, value, ))
    bot.reply_to(message,text)

@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise ConvertionException('Неверно указаны параметры')
        quote, base, amount = values
        result = APIException.convert(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Бот не может обработать команду\n{e}')
    else:
        result = result['conversion_result']
        text = f'Цена {amount} {quote} в {base} - {result}'
        bot.send_message(message.chat.id, text)
    print(message.text, message.chat.username)



bot.polling(none_stop=True)