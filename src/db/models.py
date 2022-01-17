from src.db.db import Base

from sqlalchemy import Column, String, Integer


class NotifyList(Base):
    __tablename__ = 'notify_list'

    id = Column(Integer, primary_key=True)
    discord_username = Column(String, nullable=False)
    mention = Column(String, nullable=False)
    github_username = Column(String, nullable=False)

    def __init__(self, discord_username: str, github_username: str, mention: str):
        self.discord_username = discord_username
        self.github_username = github_username
        self.mention = mention

    def __repr__(self) -> str:
        return f'NotifyList({self.discord_username}, {self.github_username})'
