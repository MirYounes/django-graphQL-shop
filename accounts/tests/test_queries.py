from django.contrib.auth import get_user_model
from graphql_jwt.testcases import JSONWebTokenTestCase


class AcoountQueriesTests(JSONWebTokenTestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            email="test@gmail.com",
            password="test"
        )

        self.client.authenticate(self.user)
    
    def test_query_get_user(self):
        query = """
            query{
                user{
                    id
                    username
                }
            }
        """

        response = self.client.execute(query)
        data = response.data['user']

        self.assertEqual(str(self.user.id),data['id'])
        self.assertEqual(self.user.username,data['username'])