import os
from dotenv import load_dotenv

#loading enviromental vairables

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI=os.getenv("DATABASE_URL")
    SQLACHEMY_TRACK_MODIFICATIONS=False
    SECRET_KEY="secret"