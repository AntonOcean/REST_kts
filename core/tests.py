import json

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient


from django.contrib.auth.models import User

from core.models import Topic
from core.serializers import TopicSerializer


class BaseViewTest(APITestCase):
    client = APIClient()

    @staticmethod
    def create_topic(title="", body="", creator_id=None):
        if title != "" and body != "" and creator_id:
            Topic.objects.create(title=title, body=body, creator_id=creator_id)

    def login_a_user(self, username="", password=""):
        url = reverse(
            "auth-login",
        )
        return self.client.post(
            url,
            data=json.dumps({
                "username": username,
                "password": password
            }),
            content_type="application/json"
        )

    def login_client(self, username="", password=""):
        # get a token from DRF
        response = self.client.post(
            reverse('create-token'),
            data=json.dumps(
                {
                    'username': username,
                    'password': password
                }
            ),
            content_type='application/json'
        )
        self.token = response.data['token']
        # set the token in the header
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.token
        )
        self.client.login(username=username, password=password)

        return self.token

    def setUp(self):
        # add test data
        self.user = User.objects.create_superuser(
            username="test_user",
            email="test@mail.com",
            password="testing",
            first_name="test",
            last_name="user",
        )
        self.create_topic("like glue", "sean paul", self.user.id)
        self.create_topic("simple song", "konshens", self.user.id)
        self.create_topic("love is wicked", "brick and lace", self.user.id)
        self.create_topic("jam rock", "damien marley", self.user.id)

class AuthLoginUserTest(BaseViewTest):
    """
    Tests for the auth/login/ endpoint
    """

    def test_login_user_with_valid_credentials(self):
        # test login with valid credentials
        response = self.login_a_user("test_user", "testing")
        # assert token key exists
        self.assertIn("token", response.data)
        # assert status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # test login with invalid credentials
        response = self.login_a_user("anonymous", "pass")
        # assert status code is 401 UNAUTHORIZED
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        url = reverse(
            "auth-login",
        )
        response = self.client.post(
            url,
            data=json.dumps({
                "useame": "test_user",
                "passrd": "testing"
            }),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class GetCreateTopicsTest(BaseViewTest):
    def test_login_user(self):
        true_data = {
            'username': 'test_user',
            'password': 'testing'
        }
        response = self.client.post(
            reverse("auth-login"),
            data=true_data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        bad_data = {
            'username': 'test title',
            'password': 'test test'
        }
        response = self.client.post(
            reverse("auth-login"),
            data=bad_data
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_new_topics(self):
        true_data = {
            'title': 'test title',
            'body': 'test test'
        }
        response = self.client.post(
            reverse("topic-create"),
            data=json.dumps(true_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.login_client('test_user', 'testing')
        len_before = Topic.objects.count()
        response = self.client.post(
            reverse("topic-create"),
            data=json.dumps(true_data),
            content_type='application/json'
        )
        len_after = Topic.objects.count()
        self.assertEqual(len_after, len_before + 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        bad_data = {
            'totle': 'test title',
            'body': 'test test'
        }
        response = self.client.post(
            reverse("topic-create"),
            data=json.dumps(bad_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_all_topics(self):
        """
        This test ensures that all songs added in the setUp method
        exist when we make a GET request to the topic.list/ endpoint
        """
        # hit the API endpoint
        response = self.client.get(
            reverse("topic-list")
        )
        # fetch the data from db
        expected = Topic.objects.all()
        serialized = TopicSerializer(expected, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
