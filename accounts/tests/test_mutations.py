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

    def test_create_user_mutation(self):
        query = """
            mutation createUser($username:String!,$email:String!,$password:String!,$first_name:String!,$last_name:String!,$is_provider:Boolean!){
                createUser(userData:{
                        username:$username
                        email:$email
                        password:$password
                        firstName:$first_name
                        lastName:$last_name
                        isProvider:$is_provider
                    }){
                    response
                }
            }
        """
        variables = {
            'username': 'create_user',
            'password': 'CreateUser5471',
            'email': 'create_user@gmail.com',
            'first_name': 'create_user',
            'last_name': 'create_user',
            'is_provider':False
        }

        response = self.client.execute(query, variables)
        data = response.data['createUser']

        self.assertEqual(data['response']['ok'], True)
        self.assertEqual(
            get_user_model().objects.get(email=variables['email']).username, variables['username'])
        self.assertEqual(
            get_user_model().objects.get(email=variables['email']).is_active, False)

    def test_mutation_change_email(self):
        query="""
            mutation changeEmail($email:String!){
                changeEmail(email:$email){
                    response
                }
            }
        """
        variables={'email':'change_email@gmail.com'}

        response = self.client.execute(query, variables)
        data = response.data['changeEmail']

        self.assertEqual(data['response']['ok'], True)
        self.assertEqual(
            get_user_model().objects.get(email=variables['email']).email,variables['email'])
        self.assertEqual(
            get_user_model().objects.get(email=variables['email']).is_active, False)

    def test_mutation_change_password(self):
        query = """
            mutation changePassword($oldPassword:String!,$newPassword1:String!,$newPassword2:String!){
                changePassword(data:{
                    oldPassword:$oldPassword
                    newPassword1:$newPassword1
                    newPassword2:$newPassword2
                }){
                    response
                }
            }
        """
        variables={
            'oldPassword':'test',
            'newPassword1':'newPassword1',
            'newPassword2':'newPassword1',
        }

        response = self.client.execute(query, variables)
        data = response.data['changePassword']

        self.assertEqual(data['response']['ok'], True)
        self.assertEqual(
            get_user_model().objects.get(email='test@gmail.com').check_password(variables['newPassword1']),True)

    def test_mutation_update_user(self):
        query = """
            mutation updateUser($username:String!,$age:Int!){
                updateUser(userData:{username:$username},profileData:{age:$age}){
                    response
                }
            }
        """
        variables = {'username':'update_user','age':20}

        response = self.client.execute(query,variables)
        data = response.data['updateUser']

        self.assertEqual(data['response']['ok'], True)
        self.assertEqual(
            get_user_model().objects.get(email='test@gmail.com').username,variables['username'])
        self.assertEqual(
            get_user_model().objects.get(email='test@gmail.com').profile.age,variables['age'])