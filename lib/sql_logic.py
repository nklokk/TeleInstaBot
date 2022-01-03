#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3 as sl


def create_tables(database: sl.Connection):
    with database:
        database.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INT,
                followers TEXT,
                following TEXT,
                timestamp INT,
                PRIMARY KEY (user_id)
            );
        """)
