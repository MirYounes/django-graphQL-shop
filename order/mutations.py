from graphene.types.generic import GenericScalar
from graphql_jwt.decorators import login_required
import graphene
from cart.cart import Cart
from products.models import Product,Color
from .models import Order,OrderItem


class CreateOrder(graphene.Mutation):
    class Arguments:
        address = graphene.String()
	
    response = GenericScalar()

    @login_required
    def mutate(parent, info, address): 
        user = info.context.user
        items = Cart.get_cart(user_id=user.id)
        if items == []:
            return CreateOrder(response={"ok":False, "message":"cart is empty"})
        total_price = 0
        for item in items :
            total_price += float(item['price'])*int(item['quantity'])

        coupon = Cart.get_coupon_from_cart(user.id)
        discount = 0
        if coupon :
            discount = (coupon.discount / float(100)) * total_price    

        order = Order.objects.create(
            user = user,
            price = total_price-discount ,
            address = address
        )

        for item in items :
            OrderItem.objects.create(
                product = Product.objects.get(id=item['product_id']),
                
                order = order,
                color = Color.objects.get(name = item['color']),
                quantity = int(item['quantity']) 
            )
        Cart.delete_cart(user_id=user.id)
        return CreateOrder(
            response={"ok":True, "message":"order added"})


class OrderMutation(graphene.ObjectType):
    create_order = CreateOrder.Field()