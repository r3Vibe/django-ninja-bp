from ninja import ModelSchema, Schema
from ninja_jwt.schema import TokenObtainPairInputSchema
from django.contrib.auth import get_user_model
import uuid
from pydantic import EmailStr
from typing import Optional


class UserSchema(ModelSchema):
    email: EmailStr

    class Config:
        model = get_user_model()
        model_fields = ["email", "first_name", "last_name", "password"]


class UserSchemaOut(Schema):
    id: Optional[uuid.UUID]
    email: EmailStr
    first_name: str
    last_name: str
    session: Optional[str]


class TokenOut(Schema):
    access: str
    refresh: str
    user: UserSchemaOut


class Login(Schema):
    email: EmailStr
    password: str


class ErrorSchema(Schema):
    error: str



class MyTokenObtainPairOutSchema(Schema):
    refresh: str
    access: str
    user: UserSchemaOut


class MyTokenObtainPairSchema(TokenObtainPairInputSchema):
    email:EmailStr
    def output_schema(self):
        out_dict = self.get_response_schema_init_kwargs()
        out_dict.update(user=UserSchema.from_orm(self._user))
        return MyTokenObtainPairOutSchema(**out_dict)