import os
import uuid

from pony.orm import db_session

from models.Profil import Profil


# =========================================
# PATH ABSOLUT
# =========================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

UPLOAD_FOLDER = os.path.join(
    BASE_DIR,
    "uploads",
    "profil"
)

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)


# =========================================
# VALIDASI FOTO
# =========================================

ALLOWED_EXT = [
    ".jpg",
    ".jpeg",
    ".png",
    ".webp"
]

MAX_SIZE = 2 * 1024 * 1024


# =========================================
# AMBIL PROFIL SAAT INI
# =========================================

def _get_current_profil():

    rows = Profil.select()[:]

    return rows[0] if rows else None


# =========================================
# PARSE MULTIPART
# =========================================

def _parse_multipart(req):

    nama = None

    foto_bytes = None

    foto_filename = None


    form = req.get_media()


    for part in form:

        if part.name == "nama":

            nama = part.text


        elif (
            part.name == "foto"
            and part.filename
        ):

            foto_bytes = part.stream.read()

            foto_filename = part.filename


    return (
        nama,
        foto_bytes,
        foto_filename
    )


# =========================================
# SIMPAN FOTO
# =========================================

def _simpan_foto(
    foto_bytes,
    foto_filename
):

    ekstensi = os.path.splitext(
        foto_filename or ""
    )[1].lower()


    if ekstensi not in ALLOWED_EXT:

        raise ValueError(
            "Format foto tidak didukung"
        )


    if len(foto_bytes) > MAX_SIZE:

        raise ValueError(
            "Ukuran foto maksimal 2 MB"
        )


    nama_file = (
        uuid.uuid4().hex
        + ekstensi
    )


    path_file = os.path.join(
        UPLOAD_FOLDER,
        nama_file
    )


    with open(
        path_file,
        "wb"
    ) as f:

        f.write(
            foto_bytes
        )


    return nama_file


# =========================================
# HAPUS FOTO LAMA
# =========================================

def _hapus_foto_lama(
    nama_file
):

    if not nama_file:

        return


    path_file = os.path.join(
        UPLOAD_FOLDER,
        os.path.basename(
            nama_file
        )
    )


    if os.path.isfile(
        path_file
    ):

        try:

            os.remove(
                path_file
            )

        except Exception as e:

            print(
                "Gagal menghapus foto lama:",
                repr(e)
            )


# =========================================
# PROFIL CONTROLLER
# =========================================

class ProfilController:


    # =====================================
    # CREATE PROFIL
    # =====================================

    @staticmethod

    @db_session

    def create_profil(
        req,
        resp
    ):

        try:

            nama, foto_bytes, foto_filename = (
                _parse_multipart(
                    req
                )
            )


            if (
                not nama
                or not nama.strip()
            ):

                resp.status = 400

                resp.media = {

                    "success": False,

                    "message":
                        "Nama wajib diisi"

                }

                return


            nama = nama.strip()

            nama_file = None


            if foto_bytes:

                try:

                    nama_file = (
                        _simpan_foto(
                            foto_bytes,
                            foto_filename
                        )
                    )

                except ValueError as ve:

                    resp.status = 400

                    resp.media = {

                        "success": False,

                        "message":
                            str(ve)

                    }

                    return


            profil = Profil(

                nama=nama,

                foto=nama_file

            )


            resp.status = 201

            resp.media = {

                "success": True,

                "message":
                    "Profil berhasil dibuat",

                "data": {

                    "id":
                        profil.id,

                    "nama":
                        profil.nama,

                    "foto":
                        profil.foto

                }

            }


        except Exception as e:

            print(
                "ERROR CREATE PROFIL:",
                repr(e)
            )


            resp.status = 500

            resp.media = {

                "success": False,

                "message":
                    "Gagal membuat profil",

                "error":
                    str(e)

            }


    # =====================================
    # GET PROFIL
    # =====================================

    @staticmethod

    @db_session

    def get_profil(
        req,
        resp
    ):

        try:

            profil = (
                _get_current_profil()
            )


            if profil is None:

                resp.status = 404

                resp.media = {

                    "success": False,

                    "message":
                        "Profil tidak ditemukan"

                }

                return


            resp.status = 200

            resp.media = {

                "success": True,

                "data": {

                    "id":
                        profil.id,

                    "nama":
                        profil.nama,

                    "foto":
                        profil.foto

                }

            }


        except Exception as e:

            print(
                "ERROR GET PROFIL:",
                repr(e)
            )


            resp.status = 500

            resp.media = {

                "success": False,

                "message":
                    "Gagal mengambil profil",

                "error":
                    str(e)

            }


    # =====================================
    # UPDATE PROFIL
    # =====================================

    @staticmethod

    @db_session

    def update_profil(
        req,
        resp
    ):

        try:

            profil = (
                _get_current_profil()
            )


            if profil is None:

                resp.status = 404

                resp.media = {

                    "success": False,

                    "message":
                        "Profil tidak ditemukan"

                }

                return


            nama, foto_bytes, foto_filename = (
                _parse_multipart(
                    req
                )
            )


            # =============================
            # UPDATE NAMA
            # =============================

            if nama is not None:

                nama = nama.strip()


                if not nama:

                    resp.status = 400

                    resp.media = {

                        "success": False,

                        "message":
                            "Nama tidak boleh kosong"

                    }

                    return


                profil.nama = nama


            # =============================
            # UPDATE FOTO
            # =============================

            if foto_bytes:

                try:

                    nama_file_baru = (
                        _simpan_foto(
                            foto_bytes,
                            foto_filename
                        )
                    )

                except ValueError as ve:

                    resp.status = 400

                    resp.media = {

                        "success": False,

                        "message":
                            str(ve)

                    }

                    return


                _hapus_foto_lama(
                    profil.foto
                )


                profil.foto = (
                    nama_file_baru
                )


            resp.status = 200

            resp.media = {

                "success": True,

                "message":
                    "Profil berhasil diperbarui",

                "data": {

                    "id":
                        profil.id,

                    "nama":
                        profil.nama,

                    "foto":
                        profil.foto

                }

            }


        except Exception as e:

            print(
                "ERROR UPDATE PROFIL:",
                repr(e)
            )


            resp.status = 500

            resp.media = {

                "success": False,

                "message":
                    "Gagal memperbarui profil",

                "error":
                    str(e)

            }