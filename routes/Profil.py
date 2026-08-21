import falcon

from controllers.ProfilController import ProfilController


class ProfilResource:

    def on_put(self, req, resp, id):
        ProfilController.update_profil(
            req,
            resp,
            id
        )


def add_routes(app):
    app.add_route(
        "/profil/{id:int}",
        ProfilResource()
    )