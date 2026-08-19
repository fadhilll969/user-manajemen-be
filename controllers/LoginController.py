import falcon
import json
import re

from pony.orm import db_session, select
from models.Login import Login


class LoginController:

    @staticmethod
    @db_session
    def login(req, resp):

        data = json.load(req.bounded_stream)

        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            resp.status = falcon.HTTP_400
            resp.media = {
                "message": "Email dan password wajib diisi"
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

        login = select(
            l for l in Login
            if l.email == email
            and l.password == password
        ).first()

        if not login:
            resp.status = falcon.HTTP_401
            resp.media = {
                "message": "Email atau password salah"
            }
            return

        resp.status = falcon.HTTP_200
        resp.media = {
            "message": "Login berhasil",
            "login": {
                "id": login.id,
                "email": login.email
            }
        }