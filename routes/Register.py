import falcon

from controllers.RegisterController import RegisterController


class RegisterResource:

    def on_post(self, req, resp):
        RegisterController.register(req, resp)


def add_routes(app):
    app.add_route("/register", RegisterResource())