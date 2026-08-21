import falcon

from controllers.ProfilController import ProfilController


# ==========================================
# UPDATE PROFIL
# ==========================================

class ProfilResource:

    def on_put(self, req, resp, id):
        ProfilController.update_profil(
            req,
            resp,
            id
        )


# ==========================================
# GET FOTO PROFIL
# ==========================================

class ProfilFotoResource:

    def on_get(self, req, resp, filename):
        ProfilController.get_foto(
            req,
            resp,
            filename
        )


# ==========================================
# ROUTES
# ==========================================

def add_routes(app):

    # Update nama + foto
    app.add_route(
        "/profil/{id:int}",
        ProfilResource()
    )

    # Menampilkan foto
    app.add_route(
        "/uploads/profil/{filename}",
        ProfilFotoResource()
    )