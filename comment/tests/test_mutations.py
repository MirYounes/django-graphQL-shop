from blog.models import Article
from graphene_django.utils.testing import GraphQLTestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from django.conf import settings
from categories.models import Category
from products.models import Product
from comment.models import Comment
import json



class BlogQueryTests(GraphQLTestCase):
    def setUp(self) -> None:
        user = get_user_model().objects.create_user(
            username="user_test",
            email="user_test@gmail.com",
            password="user_test"
        )
        image = SimpleUploadedFile(
            name='test.jpg',
            content=open(f'{settings.STATIC_ROOT}/test/test.jpg', 'rb').read(),
            content_type='image/jpg'
        )
        self.article = Article.objects.create(
            user=user,
            title='article_test',
            slug='article_test',
            tags='article_test',
            body='article_test',
            status='article_draft',
            image=image
        )
        category = Category.objects.create(name="category_test")
        self.product = Product.objects.create(
            title='product_test',
            slug='product_test',
            price = 200.00,
            category=category,
            tags='product_test',
            description='product_test',
            image=image
        )

        self.comment=Comment.objects.create(
            rate=5,
            body='comment_test',
            fullname='comment_test',
            content_object=self.product
        )
    def test_mutation_comment_to_product(self):
        response = self.query(
            """
                mutation commentToPrdocut($objectId:ID!,$rate:Int!,$fullname:String!,$body:String!){
                    commentToProduct(data:{
                        objectId:$objectId
                        rate:$rate
                        fullname:$fullname
                        body:$body
                    }){
                        response
                    }
                }
            """,
            variables={
                'objectId':self.product.id,
                'rate':3,
                'fullname':'test_fullname',
                'body':'test_body'
            }
        )

        content = json.loads(response.content)
        data = content['data']['commentToProduct']

        self.assertEqual(data['response']['ok'],True)
        self.assertEqual(Comment.objects.count(),2)
        self.assertEqual(Comment.objects.get(id=2).object_id, 1)
        self.assertEqual(Comment.objects.get(id=2).rate, '3')

    def test_mutation_comment_to_article(self):
        response = self.query(
            """
                mutation commentToArticle($objectId:ID!,$rate:Int!,$fullname:String!,$body:String!){
                    commentToArticle(data:{
                        objectId:$objectId
                        rate:$rate
                        fullname:$fullname
                        body:$body
                    }){
                        response
                    }
                }
            """,
            variables={
                'objectId':self.article.id,
                'rate':3,
                'fullname':'test_fullname',
                'body':'test_body'
            }
        )

        content = json.loads(response.content)
        data = content['data']['commentToArticle']

        self.assertEqual(data['response']['ok'],True)
        self.assertEqual(Comment.objects.count(),2)
        self.assertEqual(Comment.objects.get(id=2).object_id, 1)
        self.assertEqual(Comment.objects.get(id=2).rate, '3')

    def test_mutation_add_reply(self):
        response = self.query(
            """
                mutation addReply($objectId:ID!,$rate:Int!,$fullname:String!,$body:String!){
                    addReply(data:{
                        objectId:$objectId
                        rate:$rate
                        fullname:$fullname
                        body:$body
                    }){
                        response
                    }
                }
            """,
            variables={
                'objectId':self.comment.id,
                'rate':3,
                'fullname':'test_fullname',
                'body':'test_body'
            }
        )

        content = json.loads(response.content)
        data = content['data']['addReply']

        self.assertEqual(data['response']['ok'],True)
        self.assertEqual(Comment.objects.count(),2)
        self.assertEqual(Comment.objects.get(id=2).object_id, 1)
        self.assertEqual(Comment.objects.get(id=2).rate, '3')