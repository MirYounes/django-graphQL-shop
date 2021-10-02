from graphene.types.generic import GenericScalar
from graphql_jwt.decorators import login_required
import graphene
from products.models import Product, Color
from .cart import Cart


class AddToCart(graphene.Mutation):
    class Arguments:
        product_id=graphene.Int(required=True)
        quantity=graphene.Int(required=True)
        color=graphene.String(required=True)
    
    response=GenericScalar()

    @login_required
    def mutate(parent, info, **kwargs):
        # get the product
        try:
            product=Product.objects.get(id=kwargs['product_id'])
        except Product.DoesNotExist:
            return AddToCart(
                response={"ok":False, "message":"product does not exist"})
        
        # check the product is available
        if not product.available:
            return AddToCart(
                response={"ok":False, "message":"product does not available"})

        # validate color
        try :
            product.color.all().get(name=kwargs['color'])
        except Color.DoesNotExist:
            return AddToCart(
                response={"ok":False, "message":"product with this color does not available"})

        # add product to cart
        Cart.add_cart(
            user_id=info.context.user.id,
            product_id=product.id,
            quantity=kwargs['quantity'],
            color = kwargs['color'],
            price=str(product.price)
        )

        return AddToCart(
            response={"ok":True, "message":"product added to cart"})      


class DeleteFromCart(graphene.Mutation):
    class Arguments:
        product_id=graphene.Int(required=True)
    
    response=GenericScalar()

    def mutate(parent, info, product_id):
        Cart.delete_product(
            user_id=info.context.user.id,
            product_id=product_id
        )

        return AddToCart(
            response={"ok":True, "message":"product deleted from cart"})  


class ClearCart(graphene.Mutation):
    response=GenericScalar()

    def mutate(parent, info):
        Cart.delete_cart(info.context.user.id)

        return AddToCart(
            response={"ok":True, "message":"cart cleared"})      
    


class CartMutation(graphene.ObjectType):
    add_to_cart = AddToCart.Field()
    delete_item=DeleteFromCart.Field()
    clear_cart=ClearCart.Field()