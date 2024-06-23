import bcrypt
from fastapi.responses import Response
from fastapi.requests import Request
from starlette_admin.auth import AdminConfig, AdminUser, AuthProvider
from starlette_admin.exceptions import FormValidationError, LoginFailed
from sqlalchemy.orm import sessionmaker

from Reflex_fastapi_with_admin.databases.database import engine
from Reflex_fastapi_with_admin.models.User import User
from Reflex_fastapi_with_admin.utils.LoggerSingleton import logger

Session = sessionmaker(bind=engine)
session = Session()


class MyAuthProvider(AuthProvider):
    """
    This is for demo purpose, it's not a better
    way to save and validate user credentials
    """
    __users = {}

    async def load_users(self):
        logger.info("Loading users")
        users = session.query(User).all()
        temp = {}
        for user in users:
            temp[user.username] = {
                "name": user.name,
                "avatar": user.avatar,
                "company_logo_url": user.company_logo_url,
                "roles": user.roles,
                "password": user.password,
            }
        self.__users = temp

    async def login(
        self,
        username: str,
        password: str,
        remember_me: bool,
        request: Request,
        response: Response,
    ) -> Response:
        if len(username) < 3:
            """Form data validation"""
            raise FormValidationError(
                {"username": "Ensure username has at least 03 characters"}
            )
        await self.load_users()
        logger.info(f"self.__users:{self.__users}")
        users = self.__users
        logger.info(f"users:{users}")
        user_db = users.get(username)
        logger.info(f"user_db:{user_db}")
        logger.info(f"users:{users}")
        logger.info(f"password:{password}")
        chk_pwd = bcrypt.checkpw(password.encode('utf-8'), user_db["password"].encode('utf-8'))

        if username in users and chk_pwd:
            """Save `username` in session"""
            request.session.update({"username": username})
            return response

        raise LoginFailed("Invalid username or password")

    async def is_authenticated(self, request) -> bool:
        if request.session.get("username", None) in self.__users:
            """
            Save current `user` object in the request state. Can be used later
            to restrict access to connected user.
            """
            request.state.user = self.__users.get(request.session["username"])
            return True

        return False

    def get_admin_config(self, request: Request) -> AdminConfig:
        user = request.state.user  # Retrieve current user
        # Update app title according to current_user
        custom_app_title = "Hello, " + user["name"] + "!"
        # Update logo url according to current_user
        custom_logo_url = None
        if user.get("company_logo_url", None):
            custom_logo_url = request.url_for("static", path=user["company_logo_url"])
        return AdminConfig(
            app_title=custom_app_title,
            logo_url=custom_logo_url,
        )

    def get_admin_user(self, request: Request) -> AdminUser:
        user = request.state.user  # Retrieve current user
        photo_url = None
        if user["avatar"] is not None:
            logger.info(f"user['avatar']:{user['avatar']}")
            user_avatar_path = f"/static/{user['avatar']}"
            logger.info(f"user_avatar_path:{user_avatar_path}")
            photo_url = str(request.url).replace("/admin/", user_avatar_path)
            #photo_url = request.url.replace("/admin/", user_avatar_path)
            # photo_url = request.url_for("/static", path=user["avatar"])
            logger.info(f"photo_url:{photo_url}")
        return AdminUser(username=user["name"], photo_url=photo_url)

    async def logout(self, request: Request, response: Response) -> Response:
        request.session.clear()
        return response