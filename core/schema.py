import graphene
from accounts.queries import AccountsQuery
from categories.queries import CategoriesQuery
from products.queries import ProductQuery
from cart.queries import CartQuery
from order.queries import OrderQuery
from blog.queries import BlogQuery
from accounts.mutations import AccountsMutation
from cart.mutations import CartMutation
from coupons.mutations import CouponMutation
from order.mutations import OrderMutation
from comment.mutations import CommentMutation


class Query(BlogQuery, OrderQuery, CartQuery, CategoriesQuery, ProductQuery, AccountsQuery, graphene.ObjectType):
    pass


class Mutation(CommentMutation, OrderMutation, CouponMutation, CartMutation, AccountsMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)