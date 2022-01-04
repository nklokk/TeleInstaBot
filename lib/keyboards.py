#!/usr/bin/python
# -*- coding: utf-8 -*-

from aiogram import types


def get_username_confirmation_keyboard(username: str):
    buttons = [
        types.InlineKeyboardButton(text='Да', callback_data='_'.join(['confirmation', 'yes', username])),
        types.InlineKeyboardButton(text='Нет', callback_data='_'.join(['confirmation', 'yes', username]))
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard


def get_menu_keyboard(username: str):
    buttons = [
        types.InlineKeyboardButton(text='Подписчики', callback_data='_'.join(['menu', 'followers', username])),
        types.InlineKeyboardButton(text='Подписки', callback_data='_'.join(['menu', 'following', username])),
        types.InlineKeyboardButton(text='Завершить', callback_data='_'.join(['menu', 'exit', username]))
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard


def get_follow_keyboard(username: str, follow: str):
    buttons = [
        types.InlineKeyboardButton(
            text='Выбрать случайного',
            callback_data='_'.join(['follow', 'random', username, follow])
        ),
        types.InlineKeyboardButton(text='Меню', callback_data='_'.join(['goto', 'menu', username]))
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    return keyboard


def get_goto_menu_keyboard(username: str):
    buttons = [
        types.InlineKeyboardButton(text='Меню', callback_data='_'.join(['goto', 'menu', username]))
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    return keyboard
