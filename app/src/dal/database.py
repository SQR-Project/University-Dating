import os

import sqlite3

from src.models.auth import VerifyAccessTokenResult
from src.models.profile import CreateProfileRequest


class Database:
    def __init__(self):
        self.db_path = os.getenv("DB_PATH")
        self.conn = sqlite3.connect(self.db_path)
        self._init_db()

    def _init_db(self):
        cursor = self.conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS profiles (
            user_id VARCHAR PRIMARY KEY,
            email VARCHAR NOT NULL,
            name VARCHAR NOT NULL,
            surname VARCHAR NOT NULL,
            age REAL NOT NULL,
            primary_interest TEXT CHECK(primary_interest IN
            ('sport', 'programming', 'music', 'reading', 'travel'))
        );""")
        self.conn.commit()

    def check(self) -> bool:
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT 1"
        )
        return cursor.fetchall() is not None

    def add_profile(
            self,
            token_data: VerifyAccessTokenResult,
            request: CreateProfileRequest
    ):
        cursor = self.conn.cursor()
        cursor.execute(
            """INSERT INTO profiles
            (user_id, email, name, surname, age, primary_interest)
            VALUES (?, ?, ?, ?, ?, ?)""",
            (
                token_data.user_id,
                token_data.email,
                request.name,
                request.surname,
                request.age,
                request.primary_interest.value
            )
        )
        self.conn.commit()

    def delete_profile(self, token_data: VerifyAccessTokenResult):
        cursor = self.conn.cursor()
        cursor.execute(
            "DELETE FROM profiles WHERE user_id = ?",
            (token_data.user_id,))
        self.conn.commit()

    def get_all_profiles(self):
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT email, name, surname, age, primary_interest FROM profiles"
        )
        return cursor.fetchall()
