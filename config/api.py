from authentication.api import AuthenticationController
from ninja_extra import NinjaExtraAPI

api = NinjaExtraAPI(
    title="Boilerplate",
    version="1.0.0",
    description="Boilerplate API",
    app_name="boilerplate",
)

api.register_controllers(AuthenticationController)
