import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

local_db = 'sqlite:///anigitbot.sqlite'

url_db = os.environ.get('DATABASE_URL', local_db)
if url_db and url_db.startswith("postgres://"):
    url_db = url_db.replace("postgres://", "postgresql://", 1)

engine = create_engine(url_db)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()
