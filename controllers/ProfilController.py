import os
import uuid

from pony.orm import db_session
from models.Profil import Profil


UPLOAD_FOLDER = "uploads/profil"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


class ProfilController:

    # =========================================
    # CREATE PROFIL
    # =========================================
    @staticmethod
    @db_session
    def create_profil(req, resp):
        try:
            nama = req.get_param("nama")

            if not nama:
                resp.status = 400
                resp.media = {
                    "success": False,
                    "message": "Nama wajib diisi"
                }
                return

            nama = nama.strip()

            if not nama:
                resp.status = 400
                resp.media = {
                    "success": False,
                    "message": "Nama tidak boleh kosong"
                }
                return

            profil = Profil(
                nama=nama
            )

            # =========================================
            # FOTO
            # =========================================
            foto = req.get_param("foto")

            if foto and foto.file:

                # Ukuran maksimal 2 MB
                foto.file.seek(0, os.SEEK_END)
                ukuran = foto.file.tell()
                foto.file.seek(0)

                if ukuran > 2 * 1024 * 1024:
                    resp.status = 400
                    resp.media = {
                        "success": False,
                        "message": "Ukuran foto maksimal 2 MB"
                    }
                    return

                # Cek ekstensi
                ekstensi = os.path.splitext(
                    foto.filename or ""
                )[1].lower()

                allowed = [
                    ".jpg",
                    ".jpeg",
                    ".png",
                    ".webp"
                ]

                if ekstensi not in allowed:
                    resp.status = 400
                    resp.media = {
                        "success": False,
                        "message": "Format foto tidak didukung"
                    }
                    return

                # Nama file random
                nama_file = uuid.uuid4().hex + ekstensi

                path_file = os.path.join(
                    UPLOAD_FOLDER,
                    nama_file
                )

                with open(path_file, "wb") as file:
                    foto.file.seek(0)
                    file.write(
                        foto.file.read()
                    )

                profil.foto = nama_file

            # =========================================
            # RESPONSE
            # =========================================
            resp.status = 201

            resp.media = {
                "success": True,
                "message": "Profil berhasil dibuat",
                "data": {
                    "id": profil.id,
                    "nama": profil.nama,
                    "foto": profil.foto
                }
            }

        except Exception as e:
            print("ERROR CREATE PROFIL:", e)

            resp.status = 500
            resp.media = {
                "success": False,
                "message": "Gagal membuat profil",
                "error": str(e)
            }

    # =========================================
    # GET PROFIL
    # =========================================
    @staticmethod
    @db_session
    def get_profil(req, resp, id):
        try:
            profil = Profil.get(id=id)

            if not profil:
                resp.status = 404
                resp.media = {
                    "success": False,
                    "message": "Profil tidak ditemukan"
                }
                return

            resp.status = 200

            resp.media = {
                "success": True,
                "data": {
                    "id": profil.id,
                    "nama": profil.nama,
                    "foto": profil.foto
                }
            }

        except Exception as e:
            print("ERROR GET PROFIL:", e)

            resp.status = 500
            resp.media = {
                "success": False,
                "message": "Gagal mengambil profil",
                "error": str(e)
            }

    # =========================================
    # UPDATE PROFIL
    # =========================================
    @staticmethod
    @db_session
    def update_profil(req, resp, id):
        try:
            profil = Profil.get(id=id)

            if not profil:
                resp.status = 404
                resp.media = {
                    "success": False,
                    "message": "Profil tidak ditemukan"
                }
                return

            # =========================================
            # UPDATE NAMA
            # =========================================
            nama = req.get_param("nama")

            if nama is not None:
                nama = nama.strip()

                if not nama:
                    resp.status = 400
                    resp.media = {
                        "success": False,
                        "message": "Nama tidak boleh kosong"
                    }
                    return

                profil.nama = nama

            # =========================================
            # UPDATE FOTO
            # =========================================
            foto = req.get_param("foto")

            if foto and foto.file:

                # Ukuran maksimal 2 MB
                foto.file.seek(0, os.SEEK_END)
                ukuran = foto.file.tell()
                foto.file.seek(0)

                if ukuran > 2 * 1024 * 1024:
                    resp.status = 400
                    resp.media = {
                        "success": False,
                        "message": "Ukuran foto maksimal 2 MB"
                    }
                    return

                # Ekstensi
                ekstensi = os.path.splitext(
                    foto.filename or ""
                )[1].lower()

                allowed = [
                    ".jpg",
                    ".jpeg",
                    ".png",
                    ".webp"
                ]

                if ekstensi not in allowed:
                    resp.status = 400
                    resp.media = {
                        "success": False,
                        "message": "Format foto tidak didukung"
                    }
                    return

                # =========================================
                # FILE BARU
                # =========================================
                nama_file = uuid.uuid4().hex + ekstensi

                path_file = os.path.join(
                    UPLOAD_FOLDER,
                    nama_file
                )

                with open(path_file, "wb") as file:
                    foto.file.seek(0)
                    file.write(
                        foto.file.read()
                    )

                # =========================================
                # HAPUS FOTO LAMA
                # =========================================
                if profil.foto:
                    foto_lama = os.path.join(
                        UPLOAD_FOLDER,
                        os.path.basename(profil.foto)
                    )

                    if os.path.exists(foto_lama):
                        try:
                            os.remove(foto_lama)
                        except Exception as e:
                            print(
                                "Gagal menghapus foto lama:",
                                e
                            )

                profil.foto = nama_file

            # =========================================
            # RESPONSE
            # =========================================
            resp.status = 200

            resp.media = {
                "success": True,
                "message": "Profil berhasil diperbarui",
                "data": {
                    "id": profil.id,
                    "nama": profil.nama,
                    "foto": profil.foto
                }
            }

        except Exception as e:
            print("ERROR UPDATE PROFIL:", e)

            resp.status = 500
            resp.media = {
                "success": False,
                "message": "Gagal memperbarui profil",
                "error": str(e)
            }