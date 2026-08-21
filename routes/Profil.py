import falcon

from controllers.ProfilController import ProfilController


class ProfilRoute:

    def on_put(self, req, resp, user_id):

        ProfilController.update_profil(
            req,
            resp,
            user_id
        )


def add_routes(app):

    app.add_route(
        "/users/{user_id:int}/profil",
        ProfilRoute()
    )