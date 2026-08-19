import falcon
from controllers.LoginController import LoginController


class LoginResource:

    def on_post(self, req, resp):
        LoginController.login(req, resp)


def add_routes(app):
    app.add_route("/login", LoginResource())