"""Welcome to Reflex! This file outlines the steps to create a basic app."""
import os

import reflex as rx

from rxconfig import config
from starlette_admin.contrib.sqla import Admin
from fastapi.middleware import Middleware
from starlette.routing import Route
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from fastapi.routing import Mount

from Reflex_fastapi_with_admin.api.api import hello, get_admin
from Reflex_fastapi_with_admin.configs.config import DATABASE_FILE, SECRET
from Reflex_fastapi_with_admin.databases.database import engine, Base
from Reflex_fastapi_with_admin.databases.seed import fill_db
from Reflex_fastapi_with_admin.DBViews.Article import ArticleView
from Reflex_fastapi_with_admin.DBViews.User import UserView
from Reflex_fastapi_with_admin.models.Article import Article
from Reflex_fastapi_with_admin.models.User import User
from Reflex_fastapi_with_admin.utils.provider import MyAuthProvider
from Reflex_fastapi_with_admin.utils.LoggerSingleton import logger

class State(rx.State):
    """The app state."""
    ...


def init_database() -> None:

    first_run = not os.path.exists(DATABASE_FILE)
    logger.info(f"First run: {first_run}")
    Base.metadata.create_all(engine)
    if first_run:
        logger.info("Filling the database")
        fill_db()


admin = Admin(
    engine,
    title="Example: Auth",
    base_url="/admin",
    statics_dir="assets/static/",
    login_logo_url="assets/static/logo.svg",  # base_url + '/statics/' + path_to_the_file
    auth_provider=MyAuthProvider(allow_paths=["assets/static/logo.svg"]),
    middlewares=[Middleware(SessionMiddleware, secret_key=SECRET)],
)


@rx.page()
def index() -> rx.Component:
    # Welcome Page (Index)
    return rx.container(
        rx.vstack(
            rx.heading("Bienvenido a reflex", size="9"),
            rx.text("Pruebas de reflex", size="5"),
        )
    )


app = rx.App(
    on_startup=[init_database()]
)
app.add_page(index)

# APIs fastAPI


# app.api.add_route(routes)
app.api.add_api_route("/", get_admin, methods=["GET"])

app.api.add_api_route("/api/hello", hello, methods=["GET"])

admin.add_view(ArticleView(Article))
admin.add_view(UserView(User))
admin.mount_to(app.api)

# mount static files
app.api.mount(
    "/static",
    StaticFiles(directory="assets/static/"),
    name="static"
)
# listar los parámetros configurados en fastAPI
logger.info(f"app.api.routes:{app.api.routes}")