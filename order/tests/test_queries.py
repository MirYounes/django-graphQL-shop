from django.contrib.auth import get_user_model
from graphql_jwt.testcases import JSONWebTokenTestCase
from categories.models import Category
from products.models import Product , Color
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from order.models import Order,OrderItem


class OrderQueryTests(JSONWebTokenTestCase):
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
        color = Color.objects.create(name="test")
        product.color.add(color)

        self.order=Order.objects.create(
            user=self.user,
            price=400,
            address="test"
        )

        OrderItem.objects.create(
            product=product,
            order=self.order,
            color=color,
            quantity=2
        )
        self.client.authenticate(self.user)
    
    def test_query_orders(self):
        query = """
            query{
                orders{
                    id
                    price
                    paid
                    items{
                        id
                        product{
                            id
                            title
                        }
                    }
                }
            }
        """
        response = self.client.execute(query)
        data = response.data['orders']
        self.assertEqual(data[0]['paid'], False)
        self.assertEqual(data[0]['price'], '400.00')
        self.assertEqual(data[0]['items'][0]['product']['id'], '1')
        self.assertEqual(data[0]['items'][0]['product']['title'], 'test')