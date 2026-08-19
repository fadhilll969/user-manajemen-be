import falcon
import json
import re

from pony.orm import db_session, select
from models.Login import Login


class RegisterController:

    @staticmethod
    @db_session
    def register(req, resp):

        data = json.load(req.bounded_stream)

        nama = data.get("nama")
        email = data.get("email")
        password = data.get("password")

        if not nama or not email or not password:
            resp.status = falcon.HTTP_400
            resp.media = {
                "message": "Nama, email, dan password wajib diisi"
            }
            return

        if not re.match(r"^[a-zA-Z0-9._%+-]+@gmail\.com$", email):
            resp.status = falcon.HTTP_400
            resp.media = {
                "message": "Email harus menggunakan @gmail.com"
            }
            return

        if len(password) < 8:
            resp.status = falcon.HTTP_400
            resp.media = {
                "message": "Password minimal 8 karakter"
            }
            return

        existing = select(
            l for l in Login if l.email == email
        ).first()

        if existing:
            resp.status = falcon.HTTP_409
            resp.media = {
                "message": "Email sudah terdaftar"
            }
            return

        Login(
            nama=nama,
            email=email,
            password=password
        )

        resp.status = falcon.HTTP_201
        resp.media = {
            "message": "Register berhasil"
        }