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

keyboard = ReplyKeyboardMarkup([['/start', '/random']], True)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def start(update, context):
    username = update.message.from_user.username

    reply_text = f''' Otmazy Bot v 0.3.5 alpha
    Привет, {username}!
    Я - альфа-версия бота для генерации отмазок.
    Сейчас я могу генерировать полуосмысленные (зато забавные) отмазки.
    Потом поумнею и начну выдавать что-то, похожее на реальность.
    Нажми /random, чтобы сгенерировать отмазку.
    '''
    update.message.reply_text(reply_text, reply_markup=keyboard)

def generate_random(update, context):
    try:
        text = test_constructor(words=df, morph=morph)
        #text = random.randint(1, 10)
        logger.info('generated text')
    except:
        text = 'whoops'
        logger.warning('failed to generate text')
    #text = 'a reply'
    update.message.reply_text(text, reply_markup=keyboard)


def main():



    updater = Updater(BOT_TOKEN, use_context=True)

    dp = updater.dispatcher

    # convhandler = ConversationHandler(
    #     entry_points=[
    #                 CommandHandler('start', start),
    #                 CommandHandler('отмазка', ask_notion_api_key),
    #                 ],

    #     states={
    #         TYPING_NOTION_API_KEY: [MessageHandler(Filters.text, set_notion_api_key)],
    #         TYPING_NOTION_PAGE_ADDRESS: [MessageHandler(Filters.text, set_page_address)],
    #     },

    #     fallbacks=[CommandHandler('done', done)],
    #     name='my_conversation',
    #     persistent=False
    # )

    # dp.add_handler(convhandler)

    start_handler = CommandHandler('start', start)
    dp.add_handler(start_handler)

    generate_v0_handler = CommandHandler('random', generate_random)
    dp.add_handler(generate_v0_handler)

    # check_client_handler = CommandHandler('check_client', check_client)
    # dp.add_handler(check_client_handler)

    # check_page_handler = CommandHandler('check_page', check_page)
    # dp.add_handler(check_page_handler)

    # send_text_to_notion_handler = MessageHandler(Filters.text, send_text_to_notion)
    # dp.add_handler(send_text_to_notion_handler)

    dp.add_error_handler(error)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
