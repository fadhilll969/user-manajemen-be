import os
import uuid
import mimetypes
import falcon

from pony.orm import db_session
from falcon import HTTPNotFound

from models.User import User


# ==========================================
# FOLDER UPLOAD
# ==========================================

UPLOAD_FOLDER = "uploads/profil"

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)


class ProfilController:

    # ==========================================
    # UPDATE PROFIL
    # ==========================================

    @staticmethod
    @db_session
    def update_profil(req, resp, id):

        try:

            # ==========================================
            # CARI USER
            # ==========================================

            user = User.get(id=id)

            if not user:

                resp.status = falcon.HTTP_404

                resp.media = {
                    "success": False,
                    "message": "User tidak ditemukan"
                }

                return

            # ==========================================
            # UPDATE NAMA
            # ==========================================

            nama = req.get_param("nama")

            if nama:

                nama = nama.strip()

                if nama:
                    user.nama = nama

            # ==========================================
            # UPDATE FOTO
            # ==========================================

            foto = req.get_param("foto")

            if foto and foto.file:

                # ==========================================
                # VALIDASI UKURAN
                # ==========================================

                foto.file.seek(
                    0,
                    os.SEEK_END
                )

                ukuran = foto.file.tell()

                foto.file.seek(0)

                if ukuran > 2 * 1024 * 1024:

                    resp.status = falcon.HTTP_400

                    resp.media = {
                        "success": False,
                        "message": "Ukuran foto maksimal 2 MB"
                    }

                    return

                # ==========================================
                # VALIDASI EXTENSION
                # ==========================================

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

                    resp.status = falcon.HTTP_400

                    resp.media = {
                        "success": False,
                        "message": "Format foto tidak didukung"
                    }

                    return

                # ==========================================
                # GENERATE NAMA FILE
                # ==========================================

                nama_file = (
                    uuid.uuid4().hex +
                    ekstensi
                )

                path_file = os.path.join(
                    UPLOAD_FOLDER,
                    nama_file
                )

                # ==========================================
                # SIMPAN FOTO BARU
                # ==========================================

                with open(
                    path_file,
                    "wb"
                ) as file:

                    foto.file.seek(0)

                    file.write(
                        foto.file.read()
                    )

                # ==========================================
                # HAPUS FOTO LAMA
                # ==========================================

                if user.foto:

                    foto_lama = os.path.join(
                        UPLOAD_FOLDER,
                        os.path.basename(
                            user.foto
                        )
                    )

                    if os.path.exists(foto_lama):

                        try:

                            os.remove(
                                foto_lama
                            )

                        except Exception as e:

                            print(
                                "GAGAL HAPUS FOTO LAMA:",
                                e
                            )

                # ==========================================
                # SIMPAN NAMA FOTO KE DATABASE
                # ==========================================

                user.foto = nama_file

            # ==========================================
            # RESPONSE
            # ==========================================

            resp.status = falcon.HTTP_200

            resp.media = {

                "success": True,

                "message": "Profil berhasil diperbarui",

                "data": {

                    "id": user.id,

                    "nama": user.nama,

                    "foto": user.foto

                }

            }

        except Exception as e:

            print(
                "ERROR UPDATE PROFIL:",
                e
            )

            resp.status = falcon.HTTP_500

            resp.media = {

                "success": False,

                "message": "Gagal memperbarui profil",

                "error": str(e)

            }


    # ==========================================
    # GET FOTO PROFIL
    # ==========================================

    @staticmethod
    def get_foto(req, resp, filename):

        try:

            # ==========================================
            # CEGAH PATH TRAVERSAL
            # ==========================================

            filename = os.path.basename(
                filename
            )

            file_path = os.path.join(
                UPLOAD_FOLDER,
                filename
            )

            # ==========================================
            # CEK FILE
            # ==========================================

            if not os.path.exists(file_path):

                raise HTTPNotFound(
                    description="Foto tidak ditemukan"
                )

            # ==========================================
            # CONTENT TYPE
            # ==========================================

            content_type, _ = mimetypes.guess_type(
                file_path
            )

            if not content_type:

                content_type = "application/octet-stream"

            resp.content_type = content_type

            # ==========================================
            # BACA FILE
            # ==========================================

            with open(
                file_path,
                "rb"
            ) as file:

                resp.data = file.read()

        except HTTPNotFound:

            raise

        except Exception as e:

            print(
                "ERROR GET FOTO:",
                e
            )

            resp.status = falcon.HTTP_500

            resp.media = {

                "success": False,

                "message": "Gagal mengambil foto",

                "error": str(e)

            }