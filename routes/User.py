from controllers.UserController import UserController


class UserResource:

    def on_get(self, req, resp):
        UserController.get_users(req, resp)

    def on_post(self, req, resp):
        UserController.create_user(req, resp)


class UserDetailResource:

    def on_get(self, req, resp, id):
        UserController.get_user(req, resp, id)

    def on_put(self, req, resp, id):
        UserController.update_user(req, resp, id)

    def on_delete(self, req, resp, id):
        UserController.delete_user(req, resp, id)


def add_routes(app):

    app.add_route("/users", UserResource())

    app.add_route("/users/{id:int}", UserDetailResource())