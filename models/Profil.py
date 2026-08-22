from pony.orm import PrimaryKey, Required, Optional

from config.database import db


class Profil(db.Entity):

    id = PrimaryKey(
        int,
        auto=True
    )

    nama = Required(str)

    foto = Optional(str)