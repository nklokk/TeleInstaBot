#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
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

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)


def get_username_confirmation_keyboard(username):
    buttons = [
        types.InlineKeyboardButton(text='Да', callback_data='confirmation_yes_' + username),
        types.InlineKeyboardButton(text='Нет', callback_data='confirmation_no_' + username)
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard


def get_menu_keyboard(username):
    buttons = [
        types.InlineKeyboardButton(text='Подписчики', callback_data='menu_followers_' + username),
        types.InlineKeyboardButton(text='Подписки', callback_data='menu_following_' + username),
        types.InlineKeyboardButton(text='Завершить', callback_data='menu_exit_' + username)
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard


def get_goto_menu_keyboard(username):
    buttons = [
        types.InlineKeyboardButton(text='Меню', callback_data='goto_menu_' + username),
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    return keyboard


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.answer('Введите username интересующего вас instagram пользователя.')


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await process_start_command(message)


@dp.message_handler()
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
            reply_markup=get_username_confirmation_keyboard(username),
            parse_mode=types.ParseMode.HTML
        )


@dp.callback_query_handler(Text(startswith='confirmation_'))
async def process_username_confirmation_callback(call: types.CallbackQuery):
    answer = call.data.split('_')[1]
    username = call.data.split('_')[2]
    if answer == 'yes':
        await call.message.edit_text(
            f'Username: <b>{username}</b>',
            reply_markup=get_menu_keyboard(username),
            parse_mode=types.ParseMode.HTML
        )
    elif answer == 'no':
        await call.message.edit_text('Введите username еще разок')


@dp.callback_query_handler(Text(startswith='goto_'))
async def process_username_confirmation_callback(call: types.CallbackQuery):
    answer = call.data.split('_')[1]
    username = call.data.split('_')[2]
    if answer == 'menu':
        await call.message.edit_text(
            f'Username: <b>{username}</b>',
            reply_markup=get_menu_keyboard(username),
            parse_mode=types.ParseMode.HTML
        )


@dp.callback_query_handler(Text(startswith='menu_'))
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
                reply_markup=get_goto_menu_keyboard(username)
            )
        else:
            await call.message.edit_text(
                'У этого пользователя нету подписчиков =(',
                reply_markup=get_goto_menu_keyboard(username)
            )
    elif answer == 'following':
        await call.message.edit_text(
            'Будет реализовано позже',
            reply_markup=get_goto_menu_keyboard(username)
        )

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
    executor.start_polling(dp)

