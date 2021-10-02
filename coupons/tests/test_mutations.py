from django.contrib.auth import get_user_model
from graphql_jwt.testcases import JSONWebTokenTestCase
from coupons.models import Coupon
from django.core.files.uploadedfile import SimpleUploadedFile
from cart.cart import redis
from datetime import datetime



class CartMutationsTests(JSONWebTokenTestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            email="test@gmail.com",
            password="test"
        )

        self.coupon = Coupon.objects.create(code="test",valid_to=datetime.now(),discount=20)

        self.client.authenticate(self.user)
    
    def tearDown(self) -> None:
        redis.flushdb()
    
    def test_mutation_apply_coupon(self):
        query = """
            mutation applyCoupon($code:String!){
                applyCoupon(code:$code){
                    response
                }
            }
        """

        variables={'code':self.coupon.code}

        response = self.client.execute(query,variables)
        data = response.data['applyCoupon']
        self.assertEqual(data['response']['ok'],True)