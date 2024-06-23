from starlette_admin.contrib.sqla import ModelView

from Reflex_fastapi_with_admin.models.User import User

class UserView(ModelView):
    exclude_fields_from_list = [User.avatar, User.company_logo_url, User.password, User.roles]
