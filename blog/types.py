from graphene_django.types import DjangoObjectType
from .models import Article


class ArticleType(DjangoObjectType):
    class Meta:
        model = Article