from django.contrib.auth import get_user_model
from graphql_jwt.testcases import JSONWebTokenTestCase


class AcoountMutationTests(JSONWebTokenTestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            email="test@gmail.com",
            password="test"
        )

        self.client.authenticate(self.user)
    
    def test_muation_create_order(self):
        query = """
            mutation createOrder($address:String!){
                createOrder(address:$address){
                    response
                }
            }
        """
        variables={'address':'test'}

        response = self.client.execute(query,variables)
        data = response.data['createOrder']

        self.assertEqual(data['response']['ok'],False)
        self.assertEqual(data['response']['message'],'cart is empty')        