from pony.orm import PrimaryKey, Required
from config.database import db


class Login(db.Entity):
    id = PrimaryKey(int, auto=True)
    nama = Required(str)
    email = Required(str, unique=True)
    password = Required(str)