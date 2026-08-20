import os
import falcon
from waitress import serve

from config.database import db
from routes.User import add_routes
from routes.Login import add_routes as add_login_routes
from routes.Register import add_routes as add_register_routes

app = falcon.App(
    middleware=[
        falcon.CORSMiddleware(
            allow_origins="*"
        )
    ]
)

db.generate_mapping(create_tables=True)

add_routes(app)
add_login_routes(app)
add_register_routes(app)


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    serve(app, host="0.0.0.0", port=port)