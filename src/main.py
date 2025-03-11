
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Enum
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime
from dotenv import load_dotenv
import os

# folosesc dotenv pentru a cripta parola datei de baze
load_dotenv()


# Conectare la baza de date MySQL
DATABASE_URL = f"mysql+pymysql://root:{os.getenv('SQL_PASSWORD')}@127.0.0.1/todo_app"
engine = create_engine(DATABASE_URL)

# Definesc bază ORM
Base = declarative_base()


# Definesc modelului pentru tabelul `tasks`
class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    deadline = Column(DateTime, nullable=False)
    status = Column(Enum('pending', 'completed', name="status_enum"), default="pending")


# Creez tabele (dacă nu există deja)
Base.metadata.create_all(engine)

# Creeez sesiune
Session = sessionmaker(bind=engine)
session = Session()
session.close()


