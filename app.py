import os

import falcon

from waitress import serve

from falcon.media.multipart import MultipartFormHandler

from config.database import db

from routes.User import add_routes

from routes.Login import add_routes as add_login_routes

from routes.Register import add_routes as add_register_routes

from routes.Profil import add_routes as add_profil_routes


# =========================================
# CORS
# =========================================

cors = falcon.CORSMiddleware(

    allow_origins=[

        "https://user-manajemen-fe.vercel.app",

    ]

)


# =========================================
# APP
# =========================================

app = falcon.App(

    middleware=[

        cors

    ]

)


# =========================================
# STATIC FILE FOTO PROFIL
# =========================================

app.add_static_route(

    "/uploads",

    "uploads"

)


# =========================================
# MULTIPART HANDLER
# =========================================

app.req_options.media_handlers[

    falcon.MEDIA_MULTIPART

] = MultipartFormHandler()


# =========================================
# DATABASE
# =========================================

db.generate_mapping(

    create_tables=True

)


# =========================================
# ROUTES
# =========================================

add_routes(app)

add_login_routes(app)

add_register_routes(app)

add_profil_routes(app)


# =========================================
# RUN SERVER
# =========================================

if __name__ == "__main__":

    port = int(

        os.getenv(

            "PORT",

            8000

        )

    )


    serve(

        app,

        host="0.0.0.0",

        port=port

    )