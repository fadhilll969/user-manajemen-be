import os
import uuid

from pony.orm import db_session

from models.User import User


UPLOAD_FOLDER = "uploads/profil"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


class ProfilController:

    @staticmethod
    @db_session
    def update_profil(req, resp, user_id):

        try:
            # =========================
            # CARI USER
            # =========================

            user = User.get(id=user_id)

            if not user:
                resp.status = 404
                resp.media = {
                    "success": False,
                    "message": "User tidak ditemukan"
                }
                return

            # =========================
            # NAMA
            # =========================

            nama = req.get_param("nama")

            if nama:
                nama = nama.strip()

                if nama:
                    user.nama = nama

            # =========================
            # FOTO
            # =========================

            foto = req.get_param("foto")

            if foto and foto.file:

                # -------------------------
                # VALIDASI UKURAN
                # -------------------------

                foto.file.seek(0, os.SEEK_END)
                ukuran = foto.file.tell()
                foto.file.seek(0)

                max_size = 2 * 1024 * 1024

                if ukuran > max_size:

                    resp.status = 400
                    resp.media = {
                        "success": False,
                        "message": "Ukuran foto maksimal 2 MB"
                    }

                    return

                # -------------------------
                # VALIDASI FORMAT
                # -------------------------

                nama_file_lama = foto.filename or ""

                ekstensi = os.path.splitext(
                    nama_file_lama
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
                        "message": "Format foto harus JPG, JPEG, PNG, atau WEBP"
                    }

                    return

                # -------------------------
                # NAMA FILE BARU
                # -------------------------

                nama_file = (
                    uuid.uuid4().hex +
                    ekstensi
                )

                path_file = os.path.join(
                    UPLOAD_FOLDER,
                    nama_file
                )

                # -------------------------
                # SIMPAN FOTO
                # -------------------------

                with open(path_file, "wb") as file:

                    foto.file.seek(0)

                    file.write(
                        foto.file.read()
                    )

                # -------------------------
                # HAPUS FOTO LAMA
                # -------------------------

                if user.foto:

                    foto_lama = os.path.join(
                        UPLOAD_FOLDER,
                        os.path.basename(user.foto)
                    )

                    if os.path.exists(foto_lama):

                        try:
                            os.remove(foto_lama)
                        except Exception:
                            pass

                # -------------------------
                # SIMPAN NAMA FOTO
                # -------------------------

                user.foto = nama_file

            # =========================
            # RESPONSE
            # =========================

            resp.status = 200

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

            print("ERROR UPDATE PROFIL:", e)

            resp.status = 500

            resp.media = {
                "success": False,
                "message": "Gagal memperbarui profil",
                "error": str(e)
            }