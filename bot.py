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

MAX_RETRY = 10

BOT_TOKEN = os.environ.get('BOT_TOKEN_OTMAZY')

df = pd.read_excel('otgovorki.xlsx', index_col=0, sheet_name=None)
logger.info('loaded data from excel')
morph = pymorphy2.MorphAnalyzer()
logger.info('initialized Morph')

keyboard = ReplyKeyboardMarkup([['/contexts', '/random'], ['/start', '/help']], True)

context_keyboard = ReplyKeyboardMarkup([[ '/work', '/study', '/official'], ['/personal', '/family', '/health'], ['/random', '/back_to_menu']], True)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def start(update, context):
    username = update.message.from_user.username

    reply_text = f''' Otgovorki Bot v 0.2.3 alpha
    Привет, {username}!
    Я - альфа-версия бота для генерации отговорок отговорок и отмазок.
    Иногда ошибаюсь - зато смешно ;)
    Справка по моим командам: /help .
    '''
    update.message.reply_text(reply_text, reply_markup=keyboard)


def show_help(update, context):
    reply_text = f''' 
    /help - помощь по командам
    /contexts - отговорки по контекстам (работа, учеба, личные дела) alpha
    /random - случайная отговорка
    '''
    update.message.reply_text(reply_text, reply_markup=keyboard)


def go_to_contexts(update, context):
    update.message.reply_text('Выберите контекст отговорки.', reply_markup=context_keyboard)


def go_to_main_menu(update, context):
    update.message.reply_text('🆗', reply_markup=keyboard)

# def generate_with_context(update, context, cntxt):
#     try:
#         text = test_constructor(words=df, morph=morph, context=cntxt)
#         #text = random.randint(1, 10)
#         logger.info('generated not serious text')
#     except:
#         text = '¯\_(ツ)_/¯'
#         logger.warning(f'failed to generate text with context {cntxt}')
#     #text = 'a reply'
#     update.message.reply_text(text, reply_markup=keyboard)


def generate_random(update, context):
    for i in range(MAX_RETRY):
        while True:
            try:
                text = test_constructor(words=df, morph=morph)
                logger.info('generated text')
                update.message.reply_text(text, reply_markup=keyboard)
            except:
                logger.warning('failed to generate text')
                continue
            break


def generate_serious(update, context):
    for i in range(MAX_RETRY):
        while True:
            try:
                text = test_constructor(words=df, morph=morph, min_seriousness=3)
                logger.info('generated text')
                update.message.reply_text(text, reply_markup=keyboard)
            except:
                logger.warning('failed to generate text')
                continue
            break


def generate_not_serious(update, context):
    for i in range(MAX_RETRY):
        while True:
            try:
                text = test_constructor(words=df, morph=morph, max_seriousness=3)
                logger.info('generated text')
                update.message.reply_text(text, reply_markup=keyboard)
            except:
                logger.warning('failed to generate text')
                continue
            break


def generate_personal(update, context):
    for i in range(MAX_RETRY):
        while True:
            try:
                text = test_constructor(words=df, morph=morph, context='personal')
                logger.info('generated text')
                update.message.reply_text(text, reply_markup=keyboard)
            except:
                logger.warning('failed to generate text')
                continue
            break


def generate_work(update, context):
    for i in range(MAX_RETRY):
        while True:
            try:
                text = test_constructor(words=df, morph=morph, context='work')
                logger.info('generated text')
                update.message.reply_text(text, reply_markup=keyboard)
            except:
                logger.warning('failed to generate text')
                continue
            break


def generate_family(update, context):
    for i in range(MAX_RETRY):
        while True:
            try:
                text = test_constructor(words=df, morph=morph, context='family')
                logger.info('generated text')
                update.message.reply_text(text, reply_markup=keyboard)
            except:
                logger.warning('failed to generate text')
                continue
            break


def generate_study(update, context):
    for i in range(MAX_RETRY):
        while True:
            try:
                text = test_constructor(words=df, morph=morph, context='study')
                logger.info('generated text')
                update.message.reply_text(text, reply_markup=keyboard)
            except:
                logger.warning('failed to generate text')
                continue
            break


def generate_official(update, context):
    for i in range(MAX_RETRY):
        while True:
            try:
                text = test_constructor(words=df, morph=morph, context='official')
                logger.info('generated text')
                update.message.reply_text(text, reply_markup=keyboard)
            except:
                logger.warning('failed to generate text')
                continue
            break


def generate_health(update, context):
    for i in range(MAX_RETRY):
        while True:
            try:
                text = test_constructor(words=df, morph=morph, context='health')
                logger.info('generated text')
                update.message.reply_text(text, reply_markup=keyboard)
            except:
                logger.warning('failed to generate text')
                continue
            break


def main():

    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    # handlers
    dp.add_error_handler(error)

    start_handler = CommandHandler('start', start)
    dp.add_handler(start_handler)

    help_handler = CommandHandler('help', show_help)
    dp.add_handler(help_handler)

    go_to_contexts_handler = CommandHandler('contexts', go_to_contexts)
    dp.add_handler(go_to_contexts_handler)

    go_to_main_menu_handler = CommandHandler('back_to_menu', go_to_main_menu)
    dp.add_handler(go_to_main_menu_handler)

    generate_random_handler = CommandHandler('random', generate_random)
    dp.add_handler(generate_random_handler)

    generate_serious_handler = CommandHandler('serious', generate_serious)
    dp.add_handler(generate_serious_handler)

    generate_not_serious_handler = CommandHandler('not_serious', generate_not_serious)
    dp.add_handler(generate_not_serious_handler)

    generate_personal_handler = CommandHandler('personal', generate_personal)
    dp.add_handler(generate_personal_handler)

    generate_family_handler = CommandHandler('family', generate_family)
    dp.add_handler(generate_family_handler)

    generate_work_handler = CommandHandler('work', generate_work)
    dp.add_handler(generate_work_handler)

    generate_study_handler = CommandHandler('study', generate_study)
    dp.add_handler(generate_study_handler)

    generate_official_handler = CommandHandler('official', generate_official)
    dp.add_handler(generate_official_handler)

    generate_health_handler = CommandHandler('health', generate_health)
    dp.add_handler(generate_health_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
