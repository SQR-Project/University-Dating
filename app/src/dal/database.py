import os

import sqlite3

from app.src.models.auth import VerifyAccessTokenResult
from app.src.models.profile import CreateProfileRequest


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
            liked_profiles VARCHAR NOT NULL,
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
            (user_id,
            email,
            name,
            surname,
            age,
            liked_profiles,
            primary_interest)
            VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (
                token_data.user_id,
                token_data.email,
                request.name,
                request.surname,
                request.age,
                token_data.email,
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
            """SELECT email,
                      name,
                      surname,
                      age,
                      liked_profiles,
                      primary_interest
                      FROM profiles"""
        )
        return cursor.fetchall()

    def get_profile_likes_by_user_id(self, user_id: str):
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT liked_profiles, FROM profiles WHERE user_id = ?",
            (user_id)
        )
        return cursor.fetchall()

    def unsafe_get_profile_by_email(self, email: str):
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT user_id FROM profiles WHERE email = ?",
            (email)
        )
        return cursor.fetchall()

    def update_profile_likes(
            self,
            token_data: VerifyAccessTokenResult,
            updated_likes: str
    ):
        cursor = self.conn.cursor()
        cursor.execute(
            """UPDATE profiles
            SET liked_profiles = ? WHERE user_id = ?""",
            (
                token_data.user_id,
                updated_likes
            )
        )
        self.conn.commit()
