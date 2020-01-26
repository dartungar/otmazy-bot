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

CHOOSING_OPTION_TYPE, GENDER, TENSE = range(3)

keyboard = ReplyKeyboardMarkup([['/contexts', '/random', '/crazy', '/nonsense'], ['/start', '/help', '/options']], True)

context_keyboard = ReplyKeyboardMarkup([['/work', '/study', '/health'], ['/personal', '/family', '/leisure'], ['/back']], True)

options_keyboard = ReplyKeyboardMarkup([['/my_gender'], ['/tense'], ['/back']], True)

choose_my_gender_keyboard = ReplyKeyboardMarkup([['/male'], ['/female'], ['/back']], True)

choose_tense_keyboard = ReplyKeyboardMarkup([['/past'], ['/future'], ['/past_and_future'], ['/back']], True)



def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def start(update, context):
    username = update.message.from_user.username

    if not db.check_if_user_exists(session, username):
        db.create_new_user(session, username)

    reply_text = f''' Otgovorki Bot v 0.2.7 alpha
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
    /random - отговорка в случайном контексте
    /crazy - странная отговорка
    /nonsense - полный бред!
    '''
    update.message.reply_text(reply_text, reply_markup=keyboard)


def go_to_contexts(update, context):
    update.message.reply_text('Выберите контекст отговорки 👇', reply_markup=context_keyboard)


def go_to_main_menu(update, context):
    update.message.reply_text('👌', reply_markup=keyboard)

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
    excuse_context = random.choice(['family', 'personal', 'health', 'leisure', 'work', 'study', 'official'])
    for i in range(MAX_RETRY):
        try:
            text = test_constructor(words=df, morph=morph, context=excuse_context)
            logger.info('generated text')
            update.message.reply_text(text, reply_markup=keyboard)
        except:
            logger.warning('failed to generate text')
            continue
        else:
            break


def generate_crazy(update, context):
    for i in range(MAX_RETRY):
        try:
            text = test_constructor(words=df, morph=morph)
            logger.info('generated text')
            update.message.reply_text(text, reply_markup=keyboard)
        except:
            logger.warning('failed to generate text')
            continue
        else:
            break



def generate_nonsense(update, context):
    for i in range(MAX_RETRY):
        try:
            text = test_constructor(words=df, morph=morph, is_nonsense=True)
            logger.info('generated text')
            update.message.reply_text(text, reply_markup=keyboard)
        except:
            logger.warning('failed to generate text')
            continue
        else:
            break


def generate_serious(update, context):
    for i in range(MAX_RETRY):
        try:
            text = test_constructor(words=df, morph=morph, min_seriousness=3)
            logger.info('generated text')
            update.message.reply_text(text, reply_markup=keyboard)
        except:
            logger.warning('failed to generate text')
            continue
        else:
            break


def generate_not_serious(update, context):
    for i in range(MAX_RETRY):
        try:
            text = test_constructor(words=df, morph=morph, max_seriousness=3)
            logger.info('generated text')
            update.message.reply_text(text, reply_markup=keyboard)
        except:
            logger.warning('failed to generate text')
            continue
        else:
            break


def generate_personal(update, context):
    for i in range(MAX_RETRY):
        try:
            text = test_constructor(words=df, morph=morph, context='personal')
            logger.info('generated text')
            update.message.reply_text(text, reply_markup=context_keyboard)
        except:
            logger.warning('failed to generate text')
            continue
        else:
            break


def generate_work(update, context):
    for i in range(MAX_RETRY):
        try:
            text = test_constructor(words=df, morph=morph, context='work')
            logger.info('generated text')
            update.message.reply_text(text, reply_markup=context_keyboard)
        except:
            logger.warning('failed to generate text')
            continue
        else:
            break


def generate_family(update, context):
    for i in range(MAX_RETRY):
        try:
            text = test_constructor(words=df, morph=morph, context='family')
            logger.info('generated text')
            update.message.reply_text(text, reply_markup=context_keyboard)
        except:
            logger.warning('failed to generate text')
            continue
        else:
            break


def generate_study(update, context):
    for i in range(MAX_RETRY):
        try:
            text = test_constructor(words=df, morph=morph, context='study')
            logger.info('generated text')
            update.message.reply_text(text, reply_markup=context_keyboard)
        except:
            logger.warning('failed to generate text')
            continue
        else:
            break


def generate_official(update, context):
    for i in range(MAX_RETRY):
        try:
            text = test_constructor(words=df, morph=morph, context='official')
            logger.info('generated text')
            update.message.reply_text(text, reply_markup=context_keyboard)
        except:
            logger.warning('failed to generate text')
            continue
        else:
            break


def generate_health(update, context):
    for i in range(MAX_RETRY):
        try:
            text = test_constructor(words=df, morph=morph, context='health')
            logger.info('generated text')
            update.message.reply_text(text, reply_markup=context_keyboard)
        except:
            logger.warning('failed to generate text')
            continue
        else:
            break


def generate_leisure(update, context):
    for i in range(MAX_RETRY):
        try:
            text = test_constructor(words=df, morph=morph, context='leisure')
            logger.info('generated text')
            update.message.reply_text(text, reply_markup=context_keyboard)
        except:
            logger.warning('failed to generate text')
            continue
        else:
            break


def options(update, context):
    update.message.reply_text('Можете задать свой пол или указать, в каком времени (прошлом\будущем) отговорка', reply_markup=options_keyboard)
    return CHOOSING_OPTION_TYPE 


def choose_my_gender(update, context):
    update.message.reply_text('Какой у вас пол? /male - мужской, /female - женский', reply_markup=choose_my_gender_keyboard)
    return GENDER


def set_my_gender_to_male(update, context):
    username = update.message.from_user.username
    user = session.query(User).filter(User.username == username).first()
    user.gender = 'male'


def set_my_gender_to_female(update, context):
    username = update.message.from_user.username
    user = session.query(User).filter(User.username == username).first()
    user.gender = 'female'


def choose_tense(update, context):
    update.message.reply_text('О каком времени должно говориться в отговорках? /past - о прошлом, /future - о будущем', reply_markup=choose_tense_keyboard)
    return TENSE


def set_tense_to_past(update, context):
    username = update.message.from_user.username
    user = session.query(User).filter(User.username == username).first()
    user.tense = 'past'


def set_tense_to_future(update, context):
    username = update.message.from_user.username
    user = session.query(User).filter(User.username == username).first()
    user.tense = 'futr'


def clean_tense(update, context):
    username = update.message.from_user.username
    user = session.query(User).filter(User.username == username).first()
    user.tense = ''




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

    go_to_main_menu_handler = CommandHandler('back', go_to_main_menu)
    dp.add_handler(go_to_main_menu_handler)

    generate_random_handler = CommandHandler('random', generate_random)
    dp.add_handler(generate_random_handler)

    generate_crazy_handler = CommandHandler('crazy', generate_crazy)
    dp.add_handler(generate_crazy_handler)

    generate_nonsense_handler = CommandHandler('nonsense', generate_nonsense)
    dp.add_handler(generate_nonsense_handler)

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
    
    generate_leisure_handler = CommandHandler('leisure', generate_leisure)
    dp.add_handler(generate_leisure_handler)

    options_handler = ConversationHandler(
        entry_points=[CommandHandler('options', options)],

        states={
            CHOOSING_OPTION_TYPE: [CommandHandler('my_gender', choose_my_gender),
                                    CommandHandler('tense', choose_tense),
                                    CommandHandler('back', go_to_main_menu)],
            GENDER: [CommandHandler('male', set_my_gender_to_male),
                        CommandHandler('female', set_my_gender_to_female),
                        CommandHandler('cancel', options)],
            TENSE: [CommandHandler('past', set_tense_to_past),
                    CommandHandler('future', set_tense_to_future),
                    CommandHandler('past_and_future', clean_tense),
                    CommandHandler('cancel', options)]
        },

        fallbacks=[CommandHandler('back', go_to_main_menu)]
    )
    dp.add_handler(options_handler)

    

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
