# encoding: utf-8

import logging

# Telegram API framework core imports
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Update
from telegram.ext import CallbackContext

# Bot constatns
from constants import *

from db import Search

# Init logger
logger = logging.getLogger(__name__)


async def delete_search(update: Update, context: CallbackContext.DEFAULT_TYPE) -> int:
    """TODO"""

    message = DELETE_SEARCH_SUCCESS_END_MESSAGE

    # extract the search id from the command
    search_id = update.message.text.replace("/ds_", "")

    # delete the search from db
    if Search.select().where(Search.id == search_id and Search.chat_id == update.message.from_user.id):
        Search.delete_by_id(search_id)

        logger.info(f'search was successfully removed: user_id:{update.message.from_user.id}, \
                  user_name: {update.message.forward_sender_name}, \
                  search_id: {search_id}')
    else:
        message = DELETE_SEARCH_FAIL_END_MESSAGE
        logger.error(f'search was not successfully removed, maybe the search id not exist or its other user search. \
                     user_id:{update.message.from_user.id}, \
                    user_name: {update.message.forward_sender_name}, \
                    search_id: {search_id}')


    buttons = [
        [
            InlineKeyboardButton(MENU_BUTTON_TEXT, callback_data=str(MENU))
        ]
    ]

    keyboard = InlineKeyboardMarkup(buttons)

    await update.message.reply_text(text=message, reply_markup=keyboard)

    return MENU