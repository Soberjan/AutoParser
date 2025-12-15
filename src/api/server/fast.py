import inspect
import os
import sys
current_dir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))  # type: ignore
parent_dir = os.path.dirname(current_dir)  # type: ignore
sys.path.insert(0, parent_dir)  # type: ignore
sys.path.append("./src")

from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI

from config import Config
Config.init()
from endpoints.analytical import *
from endpoints.technical import technical_router
from database.database import Database
from sender.sender import Sender

app = FastAPI()

db = Database()
db.connect()
db.cur.execute('SET search_path TO testing;')
# s = Sender()
# s.connect()
# app.state.sender = s
app.state.db = db

app.include_router(analytical_router)
app.include_router(applicant_router)
app.include_router(optimization_router)
app.include_router(vacancy_router)
app.include_router(progress_router)
app.include_router(technical_router)
