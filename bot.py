import logging
import os
import db
from db import session, User, create_new_user, check_if_user_exists
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

options_keyboard = ReplyKeyboardMarkup([['/my_gender'], ['/tense'], ['/exit']], True)

choose_my_gender_keyboard = ReplyKeyboardMarkup([['/male'], ['/female'], ['/cancel']], True)

choose_tense_keyboard = ReplyKeyboardMarkup([['/past'], ['/future'], ['/past_and_future'], ['/cancel']], True)


def update_user_data(update, context, session):
    print('trying to get user_data...')
    try:
        user_data = context.user_data
    except Exception as e:
        print(f"Could not get user_data: {e}")
    username = update.message.from_user.username
    try:
        user = session.query(User).filter(User.username == username).first()
    except Exception as e:
        print(f'Could not fetch user from DB: {e}')
    print(f'setting context.user_data for user {user}...')
    user_data['gender'] = user.gender
    user_data['tense'] = user.tense


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def start(update, context):
    username = update.message.from_user.username

    if not db.check_if_user_exists(session, username):
        db.create_new_user(session, username)

    update_user_data(update, context, session)

    reply_text = f''' Otgovorki Bot v 0.3.0 alpha
    Привет, {username}!
    Я - альфа-версия бота для генерации отговорок отговорок и отмазок.
    Иногда ошибаюсь - зато смешно ;)
    Справка по моим командам: /help .
    '''
    update.message.reply_text(reply_text, reply_markup=keyboard)
    return ConversationHandler.END


def show_help(update, context):
    reply_text = f''' 
    /help - помощь по командам
    /options - настройки отговорок
    /contexts - отговорки по контекстам (работа, учеба, личные дела) alpha
    /random - отговорка в случайном контексте
    /crazy - странная отговорка
    /nonsense - полный бред!
    '''
    update.message.reply_text(reply_text, reply_markup=keyboard)
    return ConversationHandler.END


def go_to_contexts(update, context):
    update.message.reply_text('Выберите контекст отговорки 👇', reply_markup=context_keyboard)


def go_to_main_menu(update, context):
    update.message.reply_text('👌', reply_markup=keyboard)


def exit_options(update, context):
    update.message.reply_text('👌', reply_markup=keyboard)
    return ConversationHandler.END


def generate_random(update, context):
    excuse_context = random.choice(['family', 'personal', 'health', 'leisure', 'work', 'study', 'official'])
    for i in range(MAX_RETRY):
        try:
            text = test_constructor(words=df, morph=morph, context=excuse_context, subj_sex=context.user_data['gender'], tense=context.user_data['tense'])
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
            text = test_constructor(words=df, morph=morph, min_seriousness=3, subj_sex=context.user_data['gender'], tense=context.user_data['tense'])
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
            text = test_constructor(words=df, morph=morph, max_seriousness=3, subj_sex=context.user_data['gender'], tense=context.user_data['tense'])
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
            text = test_constructor(words=df, morph=morph, context='personal', subj_sex=context.user_data['gender'], tense=context.user_data['tense'])
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
            text = test_constructor(words=df, morph=morph, context='work', subj_sex=context.user_data['gender'], tense=context.user_data['tense'])
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
            text = test_constructor(words=df, morph=morph, context='family', subj_sex=context.user_data['gender'], tense=context.user_data['tense'])
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
            text = test_constructor(words=df, morph=morph, context='study', subj_sex=context.user_data['gender'], tense=context.user_data['tense'])
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
            text = test_constructor(words=df, morph=morph, context='official', subj_sex=context.user_data['gender'], tense=context.user_data['tense'])
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
            text = test_constructor(words=df, morph=morph, context='health', subj_sex=context.user_data['gender'], tense=context.user_data['tense'])
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
            text = test_constructor(words=df, morph=morph, context='leisure', subj_sex=context.user_data['gender'], tense=context.user_data['tense'])
            logger.info('generated text')
            update.message.reply_text(text, reply_markup=context_keyboard)
        except:
            logger.warning('failed to generate text')
            continue
        else:
            break


def options(update, context):
    username = update.message.from_user.username
    user = session.query(User).filter(User.username == username).first()
    update.message.reply_text(f'Установлен пол: {user.gender}, время - {user.tense}. Можете задать свой пол или указать, в каком времени (прошлом, будущем) отговорка', reply_markup=options_keyboard)
    return CHOOSING_OPTION_TYPE 


def choose_my_gender(update, context):
    update.message.reply_text('/male - мужской, /female - женский', reply_markup=choose_my_gender_keyboard)
    return GENDER


def set_my_gender_to_male(update, context):
    username = update.message.from_user.username
    user = session.query(User).filter(User.username == username).first()
    user.gender = 'male'
    session.commit()
    update.message.reply_text('Установлен мужской пол!', reply_markup=keyboard)
    return ConversationHandler.END


def set_my_gender_to_female(update, context):
    username = update.message.from_user.username
    user = session.query(User).filter(User.username == username).first()
    user.gender = 'female'
    session.commit()
    update.message.reply_text('Установлен женский пол!', reply_markup=keyboard)
    return ConversationHandler.END


def choose_tense(update, context):
    update.message.reply_text('О каком времени должно говориться в отговорках? /past - о прошлом, /future - о будущем', reply_markup=choose_tense_keyboard)
    return TENSE


def set_tense_to_past(update, context):
    username = update.message.from_user.username
    user = session.query(User).filter(User.username == username).first()
    user.tense = 'past'
    session.commit()
    update.message.reply_text('Установлено прошедшее время!', reply_markup=keyboard)
    return ConversationHandler.END


def set_tense_to_future(update, context):
    username = update.message.from_user.username
    user = session.query(User).filter(User.username == username).first()
    user.tense = 'futr'
    session.commit()
    update.message.reply_text('Установлено будущее время!', reply_markup=keyboard)
    return ConversationHandler.END


def clean_tense(update, context):
    username = update.message.from_user.username
    user = session.query(User).filter(User.username == username).first()
    user.tense = ''
    session.commit()
    update.message.reply_text('Установлены прошедшее и будущее времена!', reply_markup=keyboard)
    return ConversationHandler.END




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
                                    CommandHandler('tense', choose_tense)],

            GENDER: [CommandHandler('male', set_my_gender_to_male),
                        CommandHandler('female', set_my_gender_to_female),
                        CommandHandler('cancel', options)],

            TENSE: [CommandHandler('past', set_tense_to_past),
                    CommandHandler('future', set_tense_to_future),
                    CommandHandler('past_and_future', clean_tense),
                    CommandHandler('cancel', options)]
        },

        fallbacks=[CommandHandler('exit', exit_options)]
    )
    dp.add_handler(options_handler)

    

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
