import os
import falcon
from waitress import serve
from falcon.media.multipart import MultipartFormHandler
from config.database import db
from routes.User import add_routes
from routes.Login import add_routes as add_login_routes
from routes.Register import add_routes as add_register_routes
from routes.Profil import add_routes as add_profil_routes

cors = falcon.CORSMiddleware(
    allow_origins=[
        "https://user-manajemen-fe.vercel.app",
    ]
)


app = falcon.App(
    middleware=[
        cors
    ]
)

# WAJIB: tanpa ini, req.get_media() untuk multipart/form-data
# (dipakai upload foto profil di ProfilController.py) tidak akan bisa diparse.
app.req_options.media_handlers[falcon.MEDIA_MULTIPART] = MultipartFormHandler()


db.generate_mapping(create_tables=True)

add_routes(app)
add_login_routes(app)
add_register_routes(app)
add_profil_routes(app)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))

    serve(
        app,
        host="0.0.0.0",
        port=port
    )