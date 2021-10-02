from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from graphene.types.generic import GenericScalar
from graphql_jwt.decorators import login_required
import graphene
import graphql_jwt
from . import types
from .utils import get_from_redis, delete_from_redis
from .tasks import send_email_task


User = get_user_model()


class CreateUser(graphene.Mutation):
    class Arguments:
        user_data = types.UserInput(required=True)

    user = graphene.Field(types.UserType)
    response = GenericScalar()

    def mutate(parent, info, user_data):
        # vlaidate email
        try:
            validate_email(user_data.email)
        except ValidationError:
            return CreateUser(
                response={"ok": False, 'message': 'Enter a valid e-mail address.'})

        # get or create user with this email
        user = None
        try:
            user = User.objects.get(email=user_data.email)
            if user.is_active:
                return CreateUser(response={
                    "ok": False, "message": "user with this email already exist"})

        except User.DoesNotExist:
            # vlaidate password
            try:
                validate_password(user_data.password)
            except ValidationError:
                return CreateUser(
                    response={"ok": False, 'message': 'Enter a valid password address.'})

            user = User.objects.create_user(
                username=user_data.username,
                email=user_data.email,
                password=user_data.password,
                is_active=False,
                first_name=user_data.first_name,
                last_name=user_data.last_name
            )

        send_email_task.delay(
            id=user.id,
            username=user.username,
            email=user.email,
            state='register',
            prefix='verify_email'
        )

        return CreateUser(
            user=user,
            response={"ok": True, "message": "user created"}
        )


class ActiveUser(graphene.Mutation):
    class Arguments:
        email = graphene.String(required=True)
        token = graphene.String(required=True)

    user = graphene.Field(types.UserType)
    response = GenericScalar()

    def mutate(parent, info, email, token):
        user = None
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return ActiveUser(
                response={"ok": False, "message": "user with this email does not exist"})

        redis_token = get_from_redis(user.id, 'register')
        if not redis_token:
            return ActiveUser(
                response={"ok": False, "message": "expired token"})
        if token != redis_token.decode('utf-8'):
            return ActiveUser(
                response={"ok": False, "message": "expired token"})

        user.is_active = True
        user.save()
        delete_from_redis(user.id, 'register')

        return ActiveUser(
            user=user,
            response={"ok": True, "message": "user actived"}
        )


class ChangeEmail(graphene.Mutation):
    class Arguments:
        email = graphene.String(required=True)

    response = GenericScalar()

    @login_required
    def mutate(parent, info, email):
        # vlaidate email
        try:
            validate_email(email)
        except ValidationError:
            return ChangeEmail(
                response={"ok": False, 'message': 'Enter a valid e-mail address.'})

        # validate unique email
        if User.objects.filter(email=email):
            return ChangeEmail(
                response={"ok": False, 'message': 'another user with tihs email exist'})

        # change the email and send veify code the new email
        user = info.context.user
        user.email = email
        user.is_active = False
        user.save()
        send_email_task.delay(
            id=user.id,
            username=user.username,
            email=email,
            state='change_email',
            prefix='verify_email'
        )

        return ChangeEmail(
            response={"ok": True, 'message': 'email changed , veify email address'})


class VerifyEmail(graphene.Mutation):
    class Arguments:
        email = graphene.String(required=True)
        token = graphene.String(required=True)

    user = graphene.Field(types.UserType)
    response = GenericScalar()

    def mutate(parent, info, email, token):
        # get the user with email
        user = None
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return VerifyEmail(
                response={"ok": False, "message": "user with this email does not exist"})

        # validate token
        redis_token = get_from_redis(user.id, 'change_email')
        if not redis_token:
            return VerifyEmail(
                response={"ok": False, "message": "expired token"})
        if token != redis_token.decode('utf-8'):
            return VerifyEmail(
                response={"ok": False, "message": "expired token"})

        # activate user
        user.is_active = True
        user.save()
        delete_from_redis(user.id, 'change_email')

        return VerifyEmail(
            user=user,
            response={"ok": True, "message": "email verified"}
        )


class ChangePasword(graphene.Mutation):
    class Arguments:
        data = types.ChangePasswordInput(required=True)

    response = GenericScalar()

    @login_required
    def mutate(parent, info, data):
        user = info.context.user

        # validate old_password
        if not user.check_password(data.old_password):
            return ChangePasword(
                response={"ok": False, "message": "old_password does not equal"})
        
        # vlaidate new password
        if data.new_password1 != data.new_password2:
            return ChangePasword(
                response={"ok": False, "message": "passwords must match"})
        
        try :
            validate_password(data.new_password1)
        except ValidationError:
            return ChangePasword(
                response={"ok": False, "message": "invalid password"})            

        # change password
        user.set_password(data.new_password1)
        user.save()
        return ChangePasword(
            response={"ok": True, "message": "password changed"})


class ResetPassword(graphene.Mutation):
    class Arguments:
        email = graphene.String(required=True)
    
    response = GenericScalar()

    def mutate(parent, info, email):
        # get user with email
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return ResetPassword(
                response={"ok":False, "message":"user with that email does not exist"})
        
        # send email
        send_email_task.delay(
            id=user.id,
            username=user.username,
            email=email,
            state='reset_password',
            prefix='verify_email'
        )

        return ResetPassword(
            response={"ok":True, "message":"please check your email"})


class SetNewPassword(graphene.Mutation):
    class Arguments:
        email = graphene.String(required=True)
        token = graphene.String(required=True)
        new_password = graphene.String(required=True)

    response = GenericScalar()

    def mutate(parent, info, email, token , new_password):
        # get the user with email
        user = None
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return SetNewPassword(
                response={"ok": False, "message": "user with this email does not exist"})

        # validate token
        redis_token = get_from_redis(user.id, 'reset_password')
        if not redis_token:
            return SetNewPassword(
                response={"ok": False, "message": "expired token"})
        if token != redis_token.decode('utf-8'):
            return SetNewPassword(
                response={"ok": False, "message": "expired token"})
        
        # validate password
        try:
            validate_password(new_password)
        except ValidationError:
            return SetNewPassword(
                response={"ok": False, "message": "invlaid password"})
        
        # set new password
        user.set_password(new_password)
        user.save()
        return SetNewPassword(
            response={"ok": True, "message": "password reseted"})


class UpdateUser(graphene.Mutation):
    class Arguments:
        user_data = types.UpdateUserInput(required=True)
        profile_data = types.UpdateProfileInput(required=True)
    
    user = graphene.Field(types.UserType)
    response = GenericScalar()

    @login_required
    def mutate(parent, info, user_data, profile_data):
        user = info.context.user
        profile = user.profile

        user.first_name = user_data.first_name or user.first_name
        user.last_name = user_data.last_name or user.last_name
        user.username = user_data.username or user.username
        user.save()
        
        profile.bio = profile_data.bio or profile.bio
        profile.avatar = profile_data.avatar or profile.avatar
        profile.age = profile_data.age or profile.age
        profile.save()

        return UpdateUser(
            user=user,
            response = {"ok":True, "message":"user updated"}
        )


class AccountsMutation(graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    create_user = CreateUser.Field()
    active_user = ActiveUser.Field()
    change_email = ChangeEmail.Field()
    verify_email = VerifyEmail.Field()
    change_password = ChangePasword.Field()
    reset_password = ResetPassword.Field()
    set_passwrd = SetNewPassword.Field()
    update_user = UpdateUser.Field()