from controllers.ProfilController import ProfilController


class ProfilResource:

    def on_get(self, req, resp):
        ProfilController.get_profil(req, resp)

    def on_post(self, req, resp):
        ProfilController.create_profil(req, resp)

    def on_put(self, req, resp):
        ProfilController.update_profil(req, resp)


def add_routes(app):
    app.add_route("/profil", ProfilResource())