#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import asyncio
import logging
import os
import random
import sqlite3 as sl

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters import Text
from dotenv import load_dotenv
import instabot

from lib import keyboards as kb
from lib import sql_logic
from tests import mocks


logging.basicConfig(level=logging.INFO)

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

parser = argparse.ArgumentParser(description='A program that runs a telegram bot that goes to instagram')
parser.add_argument('--mock', action='store_true', help='enable mock mode')
args = parser.parse_args()

INST_USERNAME = os.environ.get('INST_USERNAME')
INST_PASSWORD = os.environ.get('INST_PASSWORD')
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')


async def process_start_command(message: types.Message):
    await message.answer('Введите username интересующего вас instagram пользователя.')


async def process_username(message: types.Message):
    if len(message.text.split()) != 1:
        await message.answer(
            'Instagram username должен состоять из <b>одного</b> слова',
            parse_mode=types.ParseMode.HTML
        )
    else:
        username = message.text
        await message.answer(
            f'Хотите обработать аккаунт <b>{username}</b>?',
            reply_markup=kb.get_username_confirmation_keyboard(username),
            parse_mode=types.ParseMode.HTML
        )


async def process_username_confirmation_callback(call: types.CallbackQuery):
    _, answer, username = call.data.split('_')
    if answer == 'yes':
        await call.message.edit_text(
            f'Username: <b>{username}</b>',
            reply_markup=kb.get_menu_keyboard(username),
            parse_mode=types.ParseMode.HTML
        )
    elif answer == 'no':
        await call.message.edit_text('Введите username еще разок')


async def process_goto_callback(call: types.CallbackQuery):
    _, answer, username = call.data.split('_')
    if answer == 'menu':
        await call.message.edit_text(
            f'Username: <b>{username}</b>',
            reply_markup=kb.get_menu_keyboard(username),
            parse_mode=types.ParseMode.HTML
        )


async def process_follow_callback(call: types.CallbackQuery):
    _, answer, username, follow = call.data.split('_')
    if answer == 'random':
        if follow == 'followers':
            user_follow = insta_bot.get_user_followers(username)
        elif follow == 'following':
            user_follow = insta_bot.get_user_following(username)
        if user_follow:
            random_user_id = random.choice(user_follow)
            random_username = insta_bot.get_username_from_user_id(random_user_id)
            await call.message.edit_text(
                f'Выбран пользователь: <b>{random_username}</b>',
                reply_markup=kb.get_goto_menu_keyboard(username),
                parse_mode=types.ParseMode.HTML
            )
        else:
            if follow == 'followers':
                text = 'У этого пользователя нету подписчиков =('
            elif follow == 'following':
                text = 'У этого пользователя нету подписок =('
            await call.message.edit_text(
                text,
                reply_markup=kb.get_goto_menu_keyboard(username)
            )


async def process_menu_callback(call: types.CallbackQuery):
    _, answer, username = call.data.split('_')
    if answer == 'exit':
        await call.message.edit_text(
            f'Обработка аккаунта <b>{username}</b> завершена',
            parse_mode=types.ParseMode.HTML
        )
    elif answer == 'followers':
        await call.message.edit_text(
            f'Username: <b>{username}</b>',
            reply_markup=kb.get_follow_keyboard(username, 'followers'),
            parse_mode=types.ParseMode.HTML
        )
    elif answer == 'following':
        await call.message.edit_text(
            f'Username: <b>{username}</b>',
            reply_markup=kb.get_follow_keyboard(username, 'following'),
            parse_mode=types.ParseMode.HTML
        )


async def start_telegram_bot():
    telegram_bot = Bot(token=TELEGRAM_TOKEN)
    try:
        disp = Dispatcher(telegram_bot)
        # register message handlers
        disp.register_message_handler(process_start_command, commands={'start', 'help'})
        disp.register_message_handler(process_username)
        # register callback query handlers
        disp.register_callback_query_handler(process_username_confirmation_callback, Text(startswith='confirmation_'))
        disp.register_callback_query_handler(process_goto_callback, Text(startswith='goto_'))
        disp.register_callback_query_handler(process_menu_callback, Text(startswith='menu_'))
        disp.register_callback_query_handler(process_follow_callback, Text(startswith='follow_'))
        await disp.start_polling()
    finally:
        await telegram_bot.close()


async def start_update_db():
    cnt = 0
    while True:
        print('{} seconds passed'.format(cnt))
        cnt += 10
        await asyncio.sleep(10)


async def main():
    tasks = [
        asyncio.create_task(start_telegram_bot()),
        asyncio.create_task(start_update_db())
    ]
    await asyncio.wait(tasks)


if __name__ == '__main__':
    global users_db, insta_bot
    if args.mock:
        insta_bot = mocks.MockInstagramBot()
        users_db = sl.connect('db/test_users.db')
    else:
        insta_bot = instabot.Bot()
        users_db = sl.connect('db/users.db')
    sql_logic.create_tables(users_db)
    insta_bot.login(username=INST_USERNAME, password=INST_PASSWORD)
    asyncio.run(main())
