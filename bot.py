#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import instabot
import sqlite3 as sl
import json

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from tests import mocks


parser = argparse.ArgumentParser(description='A program that runs a telegram bot that goes to instagram')
parser.add_argument('--mock', action='store_true', help='enable mock mode')
args = parser.parse_args()

# ----------
INST_USERNAME = "fukziav@mail.ru"
INST_PASSWORD = "y#Us)r(j2\cH2nL/l@k2]>DWIV)~vC't/<Nrlk:j"
TOKEN = '1034004944:AAEYHq_czZ77r-XxiE34rXvDDuu53fizyHc'
# ----------

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


def insert_or_update_user_id(user_id, username, user_followers):
    user_followers = json.dumps(user_followers)
    with users_db:
        info = users_db.execute(f'SELECT * FROM users WHERE user_id = {user_id}').fetchone()
        if info is not None:
            users_db.execute('UPDATE users SET followers = ?, username = ? WHERE user_id = ?', (user_followers, username, user_id))
        else:
            users_db.execute('INSERT INTO users (user_id, username, followers) VALUES (?, ?, ?)', (user_id, username, user_followers))


def get_followers_from_db(user_id):
    info = users_db.execute(f'SELECT username, followers FROM users WHERE user_id = {user_id}').fetchone()
    if info is not None:
        return (info[0], json.loads(info[1]))
    else:
        return (None, None)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    options = message.text.split()
    if len(options) == 2:
        user_id = message.from_user.id
        username = options[1]
        user_followers = insta_bot.get_user_followers(username)
        insert_or_update_user_id(user_id, username, user_followers)
        await message.reply(f'Супер!\nПривязал к тебе {username}!\nНа данный момент у этого аккаунта {len(user_followers)} подписчиков')
    else:
        await message.reply('Напиши пожалуйста "/start <никнейм в инстаграме>"')


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply('Прежде всего напиши команду "/start <никнейм в инстаграме>"')


@dp.message_handler(commands=['followers'])
async def process_followers_command(message: types.Message):
    user_id = message.from_user.id
    username, db_followers = get_followers_from_db(user_id)
    if db_followers is None:
        await bot.send_message(user_id, 'Напиши пожалуйста "/start <никнейм в инстаграме>"')
    else:
        user_followers = insta_bot.get_user_followers(username)
        insert_or_update_user_id(user_id, username, user_followers)
        delta = len(user_followers) - len(db_followers) 
        await bot.send_message(user_id, f'У аккаунта {username} подписчиков изменилось на {delta}')


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

