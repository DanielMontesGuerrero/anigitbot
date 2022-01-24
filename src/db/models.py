from src.db.db import Base

from sqlalchemy import Column, String, Integer, BigInteger


class NotifyUserList(Base):
    __tablename__ = 'notify_user_list'

    id = Column(Integer, primary_key=True)
    discord_username = Column(String, nullable=False)
    mention = Column(String, nullable=False)
    github_username = Column(String, nullable=False)

    def __init__(self, discord_username: str, github_username: str, mention: str):
        self.discord_username = discord_username
        self.github_username = github_username
        self.mention = mention

    def __repr__(self) -> str:
        return f'NotifyUserList({self.discord_username}, {self.github_username})'

class NotifyChannelList(Base):
    __tablename__ = 'notify_channel_list'

    id = Column(Integer, primary_key=True)
    discord_channel = Column(BigInteger, nullable=False)
    github_username = Column(String, nullable=False)
    github_repo = Column(String, nullable=False)

    def __init__(self, discord_channel: int, github_username: str, github_repo: str) -> None:
        self.github_username = github_username
        self.discord_channel = discord_channel
        self.github_repo = github_repo

    def __repr__(self) -> str:
        return f'NotifyChannelList({self.github_repo}, {self.discord_channel})'
