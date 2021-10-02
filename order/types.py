from graphene_django.types import DjangoObjectType
from .models import Order, OrderItem


class OrderType(DjangoObjectType):
    class Meta:
        model = Order


class OrderItemType(DjangoObjectType):
    class Meta:
        model = OrderItem