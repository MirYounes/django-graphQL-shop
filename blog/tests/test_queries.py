from django.conf import settings
import json
from blog.models import Article
from graphene_django.utils.testing import GraphQLTestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model


class BlogQueryTests(GraphQLTestCase):
    def setUp(self) -> None:
        user = get_user_model().objects.create_user(
            username="test",
            email="test@gmail.com",
            password="test"
        )
        image = SimpleUploadedFile(
            name='test.jpg',
            content=open(f'{settings.STATIC_ROOT}/test/test.jpg', 'rb').read(),
            content_type='image/jpg'
        )
        self.article = Article.objects.create(
            user=user,
            title='test',
            slug='test',
            tags='test',
            body='test',
            status='draft',
            image=image
        )
    
    def test_query_products(self):
        response=self.query(
            '''
                query{
                    articles{
                        id
                        slug
                        image
                    }
                }
            '''
        )
        content = json.loads(response.content)
        data = content['data']['articles']
        self.assertEqual(data[0]['id'],'1')
        self.assertNotEqual(data[0]['image'],None)
    
    def test_query_article(self):
        response=self.query(
            '''
                query article($id:ID!){
                    article(id:$id){
                        id
                        slug
                        image
                    }
                }
            ''',
             variables = {'id':self.article.id}
        )
       
        content = json.loads(response.content)
        data = content['data']['article']
        self.assertEqual(data['id'],'1')
        self.assertNotEqual(data['image'],None)