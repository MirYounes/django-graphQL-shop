from graphene.types.generic import GenericScalar
from graphql_jwt.decorators import login_required
import graphene
from .cart import Cart


class CartQuery(graphene.ObjectType):
    cart = GenericScalar()

    @login_required
    def resolve_cart(parent, info):
        user_id = info.context.user.id
        data = Cart.get_cart(user_id)
        total_price = 0
        for item in data:
            total_price += float(item['price'])*int(item['quantity'])

        coupon = Cart.get_coupon_from_cart(user_id)
        discount = 0
        coupon_content = None
        if coupon:
            discount = (coupon.discount / float(100)) * total_price
            coupon_content = {
                'code': coupon.code or None,
                'discount': f'{coupon.discount}% ({discount})'
            }

        content = {
            'products': data,
            'coupon': coupon_content,
            'total_price': total_price - discount
        }

        return content