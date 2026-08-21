from controllers.ProfilController import ProfilController


class ProfilResource:

    def on_get(self, req, resp, id):
        ProfilController.get_profil(
            req,
            resp,
            id
        )

    def on_put(self, req, resp, id):
        ProfilController.update_profil(
            req,
            resp,
            id
        )


class ProfilCreateResource:

    def on_post(self, req, resp):
        ProfilController.create_profil(
            req,
            resp
        )


def add_routes(app):

    # CREATE
    app.add_route(
        "/profil",
        ProfilCreateResource()
    )

    # GET + UPDATE
    app.add_route(
        "/profil/{id:int}",
        ProfilResource()
    )