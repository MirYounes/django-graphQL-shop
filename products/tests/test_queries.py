from django.conf import settings
import json
from categories.models import Category
from products.models import Product,Color
from graphene_django.utils.testing import GraphQLTestCase
from django.core.files.uploadedfile import SimpleUploadedFile


class ProductsQueryTests(GraphQLTestCase):
    def setUp(self) -> None:
        image = SimpleUploadedFile(
            name='test.jpg',
            content=open(f'{settings.STATIC_ROOT}/test/test.jpg', 'rb').read(),
            content_type='image/jpg'
        )
        category = Category.objects.create(name="test")
        self.product = Product.objects.create(
            title='test',
            slug='test',
            price = 200.00,
            category=category,
            tags='test',
            description='test',
            image=image
        )
    
    def test_query_products(self):
        response=self.query(
            '''
                query{
                    products{
                        id
                        slug
                        price
                        image
                    }
                }
            '''
        )
        content = json.loads(response.content)
        data = content['data']['products']
        self.assertEqual(data[0]['id'],'1')
        self.assertEqual(data[0]['price'],'200.00')
        self.assertNotEqual(data[0]['image'],None)
    
    def test_query_product(self):
        response=self.query(
            '''
                query product($id:ID!){
                    product(id:$id){
                        id
                        slug
                        price
                        image
                    }
                }
            ''',
             variables = {'id':self.product.id}
        )
       
        content = json.loads(response.content)
        data = content['data']['product']
        self.assertEqual(data['id'],'1')
        self.assertEqual(data['price'],'200.00')
        self.assertNotEqual(data['image'],None)