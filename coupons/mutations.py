from graphene.types.generic import GenericScalar
from graphql_jwt.decorators import login_required
import graphene
from cart.cart import Cart
from .models import Coupon


class ApplyCoupon(graphene.Mutation):
    class Arguments:
        code = graphene.String(required=True)
    
    response=GenericScalar()

    @login_required
    def mutate(parent, info, code):
        user_id = info.context.user.id

        # get the coupon
        try:
            coupon = Coupon.objects.get(code=code)
        except Coupon.DoesNotExist:
            return ApplyCoupon(
                response={"ok":False, "message":"coupon does not exist"})
        
        # delete old coupon
        Cart.delete_coupon_from_cart(user_id)

        # add new coupon
        Cart.add_coupon_to_cart(
            user_id=user_id,
            code = code
        )

        return ApplyCoupon(
            response={"ok":True, "message":"coupon applied"})


class CouponMutation(graphene.ObjectType):
    apply_coupon = ApplyCoupon.Field()