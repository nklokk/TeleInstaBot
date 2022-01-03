#!/usr/bin/python
# -*- coding: utf-8 -*-

from aiogram import types


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
