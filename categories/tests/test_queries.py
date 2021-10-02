from graphene_django.utils.testing import GraphQLTestCase
import json
from categories.models import Category


class CategoriesQueryTest(GraphQLTestCase):
    def setUp(self) -> None:
        self.category = Category.objects.create(name="test")
    
    def test_query_categories(self):
        response = self.query(
            '''query{
                    categories{
                        id
                        slug
                    }
                }
            '''
        )

        content = json.loads(response.content)
        data = content['data']['categories']

        self.assertResponseNoErrors(response)
        self.assertEqual(data[0]['id'],str(self.category.id))
        self.assertEqual(data[0]['slug'],self.category.slug)