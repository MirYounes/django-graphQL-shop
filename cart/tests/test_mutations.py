from django.contrib.auth import get_user_model
from django.db.models import query
from graphql_jwt.testcases import JSONWebTokenTestCase
from categories.models import Category
from products.models import Product 
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from cart.cart import redis


class CartMutationsTests(JSONWebTokenTestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            email="test@gmail.com",
            password="test"
        )

        image = SimpleUploadedFile(
            name='test.jpg',
            content=open(f'{settings.STATIC_ROOT}/test/test.jpg', 'rb').read(),
            content_type='image/jpg'
        )
        category = Category.objects.create(name="test")
        product = Product.objects.create(
            title='test',
            slug='test',
            price = 200.00,
            category=category,
            tags='test',
            description='test',
            image=image,
        )
        product.color.create(name="test")
        self.product=product

        self.client.authenticate(self.user)
    
    def tearDown(self) -> None:
        redis.flushdb()
    
    def test_mutation_add_to_cart(self):
        query = """
            mutation addToCart($productId:Int!,$quantity:Int!,$color:String!){
                addToCart(productId:$productId,quantity:$quantity,color:$color){
                    response
                }
            }
        """

        variables={
            'productId':self.product.id,
            'quantity':2,
            'color':'test'
        }

        response = self.client.execute(query,variables)
        data = response.data['addToCart']
        self.assertEqual(data['response']['ok'],True)
    
    def test_mutation_delete_item(self):
        query = """
            mutation deleteItem($productId:Int!){
                deleteItem(productId:$productId){
                    response
                }
            }
        """

        variables={
            'productId':self.product.id,
        }

        response = self.client.execute(query,variables)
        data = response.data['deleteItem']
        self.assertEqual(data['response']['ok'],True)
    
    def test_mutation_clear_carts(self):
        query = """
            mutation{
                clearCart{
                    response
                }
            }
        """

        response = self.client.execute(query)
        data = response.data['clearCart']
        self.assertEqual(data['response']['ok'],True)