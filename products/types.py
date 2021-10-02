from graphene_django.types import DjangoObjectType
from .models import Product,Color


class ColorType(DjangoObjectType):
    class Meta:
        model=Color


class ProductType(DjangoObjectType):
    class Meta:
        model = Product




