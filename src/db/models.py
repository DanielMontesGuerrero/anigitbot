from src.db.db import Base

from sqlalchemy import Column, String, Integer, Boolean


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    discord_username = Column(String, nullable=False)
    github_username = Column(String, nullable=False)
    notify = Column(Boolean, nullable=False, default=False)

    def __init__(self, discord_username, github_username):
        self.discord_username = discord_username
        self.github_username = github_username

    def __repr__(self) -> str:
        return f'User({self.discord_username}, {self.github_username})'

    def __str__(self) -> str:
        return self.github_username
