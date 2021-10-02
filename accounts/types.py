import graphene
from graphene_django.types import DjangoObjectType
from graphene_file_upload.scalars import Upload
from .models import User, Profile


# Types 

class ProfileType(DjangoObjectType):
    class Meta:
        model = Profile
        

class UserType(DjangoObjectType):
    class Meta:
        model = User
        exclude = ['password','is_provider']


# Inputs 

class UserInput(graphene.InputObjectType):
    first_name = graphene.String()
    last_name = graphene.String()   
    username = graphene.String(required=True)
    email = graphene.String(required=True)
    password = graphene.String(required=True)
    is_provider = graphene.Boolean(required=True)


class ChangePasswordInput(graphene.InputObjectType):
    old_password = graphene.String(required=True)
    new_password1 = graphene.String(required=True)
    new_password2 = graphene.String(required=True)


class UpdateProfileInput(graphene.InputObjectType):
    bio = graphene.String(required=False)
    avatar = Upload(required=False)
    age = graphene.Int(required=False)


class UpdateUserInput(graphene.InputObjectType):
    first_name = graphene.String()
    last_name = graphene.String()
    username = graphene.String()