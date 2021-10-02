from graphql_jwt.decorators import login_required
import graphene
from .types import UserType



class AccountsQuery(graphene.ObjectType):
    user = graphene.Field(UserType)

    @login_required
    def resolve_user(parent, info):
        user = info.context.user
        return user