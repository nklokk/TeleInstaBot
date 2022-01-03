#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import asyncio
import instabot
import json
import logging
import os
import sqlite3 as sl

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.utils import executor
from dotenv import load_dotenv
from lib import keyboards as kb
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
    answer = call.data.split('_')[1]
    username = call.data.split('_')[2]
    if answer == 'yes':
        await call.message.edit_text(
            f'Username: <b>{username}</b>',
            reply_markup=kb.get_menu_keyboard(username),
            parse_mode=types.ParseMode.HTML
        )
    elif answer == 'no':
        await call.message.edit_text('Введите username еще разок')


async def process_goto_callback(call: types.CallbackQuery):
    answer = call.data.split('_')[1]
    username = call.data.split('_')[2]
    if answer == 'menu':
        await call.message.edit_text(
            f'Username: <b>{username}</b>',
            reply_markup=kb.get_menu_keyboard(username),
            parse_mode=types.ParseMode.HTML
        )


async def process_menu_callback(call: types.CallbackQuery):
    answer = call.data.split('_')[1]
    username = call.data.split('_')[2]
    if answer == 'exit':
        await call.message.edit_text(
            f'Обработка аккаунта <b>{username}</b> завершена',
            parse_mode=types.ParseMode.HTML
        )
    elif answer == 'followers':
        user_followers = insta_bot.get_user_followers(username) 
        if user_followers:
            user_followers = [
                insta_bot.get_username_from_user_id(user_id)
                for user_id in user_followers[:5]
            ]
            await call.message.edit_text(
                '\n'.join(user_followers),
                reply_markup=kb.get_goto_menu_keyboard(username)
            )
        else:
            await call.message.edit_text(
                'У этого пользователя нету подписчиков =(',
                reply_markup=kb.get_goto_menu_keyboard(username)
            )
    elif answer == 'following':
        await call.message.edit_text(
            'Будет реализовано позже',
            reply_markup=kb.get_goto_menu_keyboard(username)
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
        await disp.start_polling()
    finally:
        await telegram_bot.close()


async def start_update_db():
    cnt = 1
    while True:
        print('{} seconds passed'.format(cnt))
        cnt += 1
        await asyncio.sleep(1)


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
    with users_db:
        users_db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INT,
                username TEXT,
                followers TEXT,
                PRIMARY KEY (user_id)
            );
        ''')
    insta_bot.login(username=INST_USERNAME, password=INST_PASSWORD)
    asyncio.run(main())

