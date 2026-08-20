import os
import falcon

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