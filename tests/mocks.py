#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
import string


class MockInstagramBot:
    def __init__(self):
        pass

    def login(self, username='', password=''):
        pass

    def get_user_followers(self, user):
        user_followers_lenght = random.randint(1, 10)
        user_followers = [random.randint(1, 100) for _ in range(user_followers_lenght)]
        return user_followers

    def get_username_from_user_id(self, user_id):
        username_lenght = random.randint(1, 10)
        username = ''.join([random.choice(string.ascii_lowercase + string.digits) for _ in range(username_lenght)])
        return username
