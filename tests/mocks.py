#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
import string


class MockInstagramBot:
    def __init__(self):
        pass

    def login(self, username='', password=''):
        pass

    def _get_random_user_ids(self):
        user_follow_len = random.randint(0, 15)
        user_follow = [random.randint(1, 10000) for _ in range(user_follow_len)]
        return user_follow

    def get_user_followers(self, user):
        return self._get_random_user_ids()

    def get_user_following(self, user):
        return self._get_random_user_ids()

    def get_username_from_user_id(self, user_id):
        username_lenght = random.randint(5, 15)
        username = ''.join([random.choice(string.ascii_lowercase + string.digits) for _ in range(username_lenght)])
        return username
