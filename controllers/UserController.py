import json
import falcon
from pony.orm import db_session

from models.User import User


class UserController:

    @staticmethod
    @db_session
    def get_users(req, resp):
        users = User.select()[:]  

        data = []

        for user in users:
            data.append({
                "id": user.id,
                "title": user.title,
                "nama": user.nama,
                "noHandphone": user.noHandphone,
                "email": user.email,
                "tanggalLahir": user.tanggalLahir,
                "role": user.role,
                "status": user.status,
                "alasanNonAktif": user.alasanNonAktif
            })

        resp.status = falcon.HTTP_200
        resp.media = {
            "message": "Data user berhasil diambil",
            "data": data
        }

    @staticmethod
    @db_session
    def get_user(req, resp, user_id):

        user = User.get(id=user_id)

        if not user:
            resp.status = falcon.HTTP_404
            resp.media = {
                "message": "User tidak ditemukan"
            }
            return

        resp.status = falcon.HTTP_200
        resp.media = {
            "message": "Data user berhasil diambil",
            "data": {
                "id": user.id,
                "title": user.title,
                "nama": user.nama,
                "noHandphone": user.noHandphone,
                "email": user.email,
                "tanggalLahir": user.tanggalLahir,
                "role": user.role,
                "status": user.status,
                "alasanNonAktif": user.alasanNonAktif
            }
        }

    @staticmethod
    @db_session
    def create_user(req, resp):

        data = json.load(req.bounded_stream)

        required_fields = [
            "title",
            "nama",
            "noHandphone",
            "email",
            "tanggalLahir",
            "role"
        ]

        for field in required_fields:
            if not data.get(field):
                resp.status = falcon.HTTP_400
                resp.media = {
                    "message": f"{field} wajib diisi"
                }
                return

        email = data.get("email")

        existing_user = User.get(email=email)

        if existing_user:
            resp.status = falcon.HTTP_409
            resp.media = {
                "message": "Email sudah digunakan"
            }
            return

        user = User(
            title=data.get("title"),
            nama=data.get("nama"),
            noHandphone=data.get("noHandphone"),
            email=email,
            tanggalLahir=data.get("tanggalLahir"),
            role=data.get("role"),
            status="active"
        )

        resp.status = falcon.HTTP_201
        resp.media = {
            "message": "User berhasil ditambahkan",
            "data": {
                "id": user.id,
                "title": user.title,
                "nama": user.nama,
                "noHandphone": user.noHandphone,
                "email": user.email,
                "tanggalLahir": user.tanggalLahir,
                "role": user.role,
                "status": user.status
            }
        }

    @staticmethod
    @db_session
    def update_user(req, resp, user_id):

        user = User.get(id=user_id)

        if not user:
            resp.status = falcon.HTTP_404
            resp.media = {
                "message": "User tidak ditemukan"
            }
            return

        data = json.load(req.bounded_stream)

        if data.get("title"):
            user.title = data["title"]

        if data.get("nama"):
            user.nama = data["nama"]

        if data.get("noHandphone"):
            user.noHandphone = data["noHandphone"]

        if data.get("email"):

            existing_user = User.get(email=data["email"])

            if existing_user and existing_user.id != user.id:
                resp.status = falcon.HTTP_409
                resp.media = {
                    "message": "Email sudah digunakan"
                }
                return

            user.email = data["email"]

        if data.get("tanggalLahir"):
            user.tanggalLahir = data["tanggalLahir"]

        if data.get("role"):
            user.role = data["role"]

        if data.get("status"):
            user.status = data["status"]

        if "alasanNonAktif" in data:
            user.alasanNonAktif = data["alasanNonAktif"]

        if data.get("password"):
            if len(data["password"]) < 8:
                resp.status = falcon.HTTP_422
                resp.media = {
                    "message": "Kata sandi minimal 8 karakter"
                }
                return
            user.password = data["password"]

        resp.status = falcon.HTTP_200
        resp.media = {
            "message": "User berhasil diperbarui"
        }

    @staticmethod
    @db_session
    def delete_user(req, resp, user_id):

        user = User.get(id=user_id)

        if not user:
            resp.status = falcon.HTTP_404
            resp.media = {
                "message": "User tidak ditemukan"
            }
            return

        user.delete()

        resp.status = falcon.HTTP_200
        resp.media = {
            "message": "User berhasil dihapus"
        }