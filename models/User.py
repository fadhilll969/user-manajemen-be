from pony.orm import PrimaryKey, Required, Optional
from config.database import db


class User(db.Entity):
    id = PrimaryKey(int, auto=True)
    title = Required(str)
    nama = Required(str)
    noHandphone = Required(str)
    email = Required(str, unique=True)
    tanggalLahir = Required(str)
    role = Required(str)
    status = Required(str, default="active")
    alasanNonAktif = Optional(str)