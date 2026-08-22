import os
import uuid

from pony.orm import db_session

from models.Profil import Profil


UPLOAD_FOLDER = "uploads/profil"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXT = [".jpg", ".jpeg", ".png", ".webp"]
MAX_SIZE = 2 * 1024 * 1024  # 2 MB


def _get_current_profil():
    """Anggap cuma ada 1 baris profil (belum ada sistem login per-user).
    Aman dari bug decompile Pony karena select() dipanggil tanpa argumen."""
    rows = Profil.select()[:]
    return rows[0] if rows else None


def _parse_multipart(req):
    """
    req.get_param() TIDAK BISA baca field dari body multipart/form-data
    (dia cuma baca query string). Field "nama" dan "foto" yang dikirim
    lewat FormData() di frontend harus dibaca lewat req.get_media(),
    yang mem-parsing body sesuai media handler yang didaftarkan di app.py
    (falcon.media.multipart.MultipartFormHandler).

    Return: (nama:str|None, foto_bytes:bytes|None, foto_filename:str|None)
    """
    nama = None
    foto_bytes = None
    foto_filename = None

    form = req.get_media()  # iterable of BodyPart

    for part in form:
        if part.name == "nama":
            nama = part.text
        elif part.name == "foto" and part.filename:
            foto_bytes = part.stream.read()
            foto_filename = part.filename

    return nama, foto_bytes, foto_filename


def _simpan_foto(foto_bytes, foto_filename):
    ekstensi = os.path.splitext(foto_filename or "")[1].lower()

    if ekstensi not in ALLOWED_EXT:
        raise ValueError("Format foto tidak didukung")

    if len(foto_bytes) > MAX_SIZE:
        raise ValueError("Ukuran foto maksimal 2 MB")

    nama_file = uuid.uuid4().hex + ekstensi
    path_file = os.path.join(UPLOAD_FOLDER, nama_file)

    with open(path_file, "wb") as f:
        f.write(foto_bytes)

    return nama_file


def _hapus_foto_lama(nama_file):
    if not nama_file:
        return
    path = os.path.join(UPLOAD_FOLDER, os.path.basename(nama_file))
    if os.path.isfile(path):
        try:
            os.remove(path)
        except Exception as e:
            print("Gagal menghapus foto lama:", repr(e))


class ProfilController:

    # =========================================
    # CREATE PROFIL
    # =========================================

    @staticmethod
    @db_session
    def create_profil(req, resp):

        try:
            nama, foto_bytes, foto_filename = _parse_multipart(req)

            if not nama or not nama.strip():
                resp.status = 400
                resp.media = {
                    "success": False,
                    "message": "Nama wajib diisi"
                }
                return

            nama = nama.strip()

            nama_file = None
            if foto_bytes:
                try:
                    nama_file = _simpan_foto(foto_bytes, foto_filename)
                except ValueError as ve:
                    resp.status = 400
                    resp.media = {"success": False, "message": str(ve)}
                    return

            profil = Profil(nama=nama, foto=nama_file)

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
    def get_profil(req, resp):

        try:
            profil = _get_current_profil()

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
    def update_profil(req, resp):

        try:
            profil = _get_current_profil()

            if profil is None:
                resp.status = 404
                resp.media = {
                    "success": False,
                    "message": "Profil tidak ditemukan"
                }
                return

            nama, foto_bytes, foto_filename = _parse_multipart(req)

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

            if foto_bytes:
                try:
                    nama_file_baru = _simpan_foto(foto_bytes, foto_filename)
                except ValueError as ve:
                    resp.status = 400
                    resp.media = {"success": False, "message": str(ve)}
                    return

                _hapus_foto_lama(profil.foto)
                profil.foto = nama_file_baru

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