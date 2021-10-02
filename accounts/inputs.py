from typing_extensions import Required
import graphene


class UserInput(graphene.InputObjectType):
    first_name = graphene.String()
    last_name = graphene.String()   
    username = graphene.String(required=True)
    email = graphene.String(required=True)
    password = graphene.String(required=True)
    is_provider = graphene.Boolean(required=True)
 