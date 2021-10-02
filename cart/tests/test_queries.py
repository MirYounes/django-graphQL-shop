from django.contrib.auth import get_user_model
from graphql_jwt.testcases import JSONWebTokenTestCase



class CartQueriesTests(JSONWebTokenTestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            email="test@gmail.com",
            password="test"
        )

        self.client.authenticate(self.user)
    
    def test_query_cart(self):
        query = """
            query{
                cart
            }
        """
        response = self.client.execute(query)
        data = response.data['cart']
        self.assertEqual(data['total_price'],0)
        self.assertEqual(data['coupon'],None)
        self.assertEqual(data['products'],[])