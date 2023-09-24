import telebot
from config import keys, TOKEN # импортируем keys, TOKEN в этот фаил
from extensions import ConvertionException, CryptoConverter # импортируем классы исключений в этот фаил

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def echo_test(message: telebot.types.Message):
    text = 'Привет, мой Дорогой друг,\n'\
           'этот Бот разработан\n'\
           'Fullstack-разработчиком на Python\n'\
           '\nБот умеет _ - _ - _ →\n'\
           'конвертировать валюту.\n'\
           '\nУвидеть доступные\n'\
           'валюты → /values\n'\
           '\nФормула записи для\n'\
           'перевода валюты → /help'
    bot.reply_to(message, text)

@bot.message_handler(commands=['help'])
def help(message: telebot.types.Message):
    text = '\nФормула записи для\n'\
           'перевода валюты:\n'\
           '\n[1] <Название валюты>'\
           '\n[2] <В какую валюту перевести>'\
           '\n[3] <Количество переводимой валюты>\n'\
           '\nПример записи:\n'\
           '.     [1]        [2]   [3]'\
           '\nДоллар Евро 24\n'\
           '\nОтвет Бота:\n'\
           'Цена 24 Доллар в Евро - 22.56\n'\
           '\nУвидеть доступные\n'\
           'валюты → /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:\n'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)
    bot.send_message(message.from_user.id, '\nФормула записи для'
                                           '\nперевода валюты → /help')

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionException('\nСлишком много параметров.\n'
                                      '\nУвидеть доступные'
                                      '\nвалюты → /values\n'
                                      '\nФормула записи для'
                                      '\nперевода валюты → /help')

        quote, base, amount = values

        total_base = CryptoConverter.convert(quote, base, amount)

    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')

    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду.\n{e}')

    else:
        text = f'Цена {amount} {quote} в {base} - {total_base} \n'\
               '\nУвидеть доступные\n'\
               'валюты → /values\n'\
               '\nФормула записи для\n'\
               'перевода валюты → /help'
        bot.send_message(message.chat.id, text)

bot.polling()
