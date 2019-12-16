import logging
import os
import db
import pandas as pd
import pymorphy2
import random
import test
from test import test_constructor
from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, ConversationHandler, Filters


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)



BOT_TOKEN = os.environ.get('BOT_TOKEN_OTMAZY')

df = pd.read_excel('otmazy_words.xlsx', index_col=0, sheet_name=None)
logger.info('loaded data from excel')
morph = pymorphy2.MorphAnalyzer()
logger.info('initialized Morph')

keyboard = ReplyKeyboardMarkup([['/start', '/help'], ['/serious', '/not_serious', '/random']], True)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def start(update, context):
    username = update.message.from_user.username

    reply_text = f''' Otmazy Bot v 0.6.0 alpha
    Привет, {username}!
    Я - альфа-версия бота для генерации отмазок.
    Сейчас я могу генерировать полуосмысленные (зато забавные) отмазки.
    Потом поумнею и начну выдавать что-то, похожее на реальность.
    Справка по моим командам: /help .
    '''
    update.message.reply_text(reply_text, reply_markup=keyboard)


def show_help(update, context):
    reply_text = f''' 
    /help - помощь по командам
    /random - случайная отмазка
    /serious - (относительно) серьезная отмазка
    /not_serious - несерьезная отмазка
    '''
    update.message.reply_text(reply_text, reply_markup=keyboard)


def generate_random(update, context):
    try:
        text = test_constructor(words=df, morph=morph)
        logger.info('generated text')
    except:
        text = 'whoops'
        logger.warning('failed to generate text')
    update.message.reply_text(text, reply_markup=keyboard)


def generate_serious(update, context):
    try:
        text = test_constructor(words=df, morph=morph, min_seriousness=3)
        #text = random.randint(1, 10)
        logger.info('generated serious text')
    except:
        text = 'whoops'
        logger.warning('failed to generate serious text')
    #text = 'a reply'
    update.message.reply_text(text, reply_markup=keyboard)


def generate_not_serious(update, context):
    try:
        text = test_constructor(words=df, morph=morph, max_seriousness=3)
        #text = random.randint(1, 10)
        logger.info('generated serious text')
    except:
        text = 'whoops'
        logger.warning('failed to generate serious text')
    #text = 'a reply'
    update.message.reply_text(text, reply_markup=keyboard)



def main():

    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    # handlers
    dp.add_error_handler(error)

    start_handler = CommandHandler('start', start)
    dp.add_handler(start_handler)

    help_handler = CommandHandler('help', show_help)
    dp.add_handler(help_handler)

    generate_random_handler = CommandHandler('random', generate_random)
    dp.add_handler(generate_random_handler)

    generate_serious_handler = CommandHandler('serious', generate_serious)
    dp.add_handler(generate_serious_handler)

    generate_not_serious_handler = CommandHandler('not_serious', generate_not_serious)
    dp.add_handler(generate_not_serious_handler)


    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
