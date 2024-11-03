from ninja_extra import ControllerBase, api_controller, route
from ninja_jwt.controller import TokenObtainPairController

from . import schema


@api_controller("/auth", tags=["Authentication"])
class AuthenticationController(ControllerBase, TokenObtainPairController):
    @route.post(
        "/register",
        description="Register a new user",
        summary="Register a new user",
        response={201: schema.UserSchemaOut},
    )
    def register(self, user: schema.UserSchema):
        from django.contrib.auth import get_user_model
        from core.models import SessionTracker, OTPCode

        """ create new user """
        new_user = get_user_model().objects.create_user(**user.dict())

        """ Create Session Tracker for new registrations """
        session = SessionTracker.objects.create(user=new_user)

        """ Create OTP Code for new registrations """
        OTPCode.objects.create(session=session)

        """ make response obj """
        res = {**new_user.__dict__, "session": session.session_token}

        return 201, res

    @route.post(
        "/login",
        response=schema.MyTokenObtainPairOutSchema,
        description="Login User",
        summary="Login User",
    )
    def obtain_token(self, user_token: schema.MyTokenObtainPairSchema):
        return user_token.output_schema()

    @route.post(
        "/verify",
        response={200: schema.GenericResponseSchema},
        description="Verify Email",
        summary="Verify Email",
    )
    def verify_email(self, code: schema.VerifyEmailSchema):
        from core.models import OTPCode, SessionTracker

        """
            Get the session by session id
            Verify the code validity
            Check for expired code or invalid code
            update the otp verification time and set is_verified to true
            update the session status
            check the attempts
            return the response
        """

        return {"message": "ok"}
