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

            if nama is None:
                resp.status = 400
                resp.media = {
                    "success": False,
                    "message": "Nama wajib diisi"
                }
                return

            nama = str(nama).strip()

            if not nama:
                resp.status = 400
                resp.media = {
                    "success": False,
                    "message": "Nama tidak boleh kosong"
                }
                return

            # =========================================
            # FOTO
            # =========================================

            foto = req.get_param("foto")
            nama_file = None

            if foto is not None and hasattr(foto, "file") and foto.file:

                # Cek ukuran
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

                # Cek nama file
                filename = getattr(foto, "filename", "") or ""

                ekstensi = os.path.splitext(filename)[1].lower()

                allowed = [".jpg", ".jpeg", ".png", ".webp"]

                if ekstensi not in allowed:
                    resp.status = 400
                    resp.media = {
                        "success": False,
                        "message": "Format foto tidak didukung"
                    }
                    return

                # Generate nama random
                nama_file = uuid.uuid4().hex + ekstensi

                path_file = os.path.join(
                    UPLOAD_FOLDER,
                    nama_file
                )

                with open(path_file, "wb") as file:
                    foto.file.seek(0)
                    file.write(foto.file.read())

            # =========================================
            # SIMPAN DATABASE
            # =========================================

            profil = Profil(
                nama=nama,
                foto=nama_file
            )

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

            print("ERROR CREATE PROFIL:", repr(e))

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

            if profil is None:
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

            print("ERROR GET PROFIL:", repr(e))

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

            if profil is None:
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

                nama = str(nama).strip()

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

            if foto is not None and hasattr(foto, "file") and foto.file:

                # Cek ukuran
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

                filename = getattr(foto, "filename", "") or ""

                ekstensi = os.path.splitext(filename)[1].lower()

                allowed = [".jpg", ".jpeg", ".png", ".webp"]

                if ekstensi not in allowed:
                    resp.status = 400
                    resp.media = {
                        "success": False,
                        "message": "Format foto tidak didukung"
                    }
                    return

                # =========================================
                # SIMPAN FOTO BARU
                # =========================================

                nama_file_baru = uuid.uuid4().hex + ekstensi

                path_file_baru = os.path.join(
                    UPLOAD_FOLDER,
                    nama_file_baru
                )

                with open(path_file_baru, "wb") as file:
                    foto.file.seek(0)
                    file.write(foto.file.read())

                # =========================================
                # HAPUS FOTO LAMA
                # =========================================

                if profil.foto:

                    foto_lama = os.path.join(
                        UPLOAD_FOLDER,
                        os.path.basename(profil.foto)
                    )

                    if os.path.isfile(foto_lama):

                        try:
                            os.remove(foto_lama)

                        except Exception as e:
                            print(
                                "Gagal menghapus foto lama:",
                                repr(e)
                            )

                profil.foto = nama_file_baru

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

            print("ERROR UPDATE PROFIL:", repr(e))

            resp.status = 500

            resp.media = {
                "success": False,
                "message": "Gagal memperbarui profil",
                "error": str(e)
            }