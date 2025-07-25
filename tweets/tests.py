from rest_framework.test import APITestCase
from .models import Tweet
from users.models import User


class TestTweetsAPI(APITestCase):

    CONTENT = "testtest"

    def setUp(self):
        user = User.objects.create(
            username="testuser",
        )
        user.set_password("0000")
        user.save()
        self.user = user

        Tweet.objects.create(
            user=self.user,
            payload=self.CONTENT,
        )

    def test_all_tweets(self):

        response = self.client.get("/api/v1/tweets/")
        data = response.json()
        self.assertEqual(
            response.status_code,
            200,
        )
        self.assertIsInstance(
            data,
            list,
        )
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["user"]["pk"], self.user.pk)
        self.assertEqual(
            data[0]["payload"],
            self.CONTENT,
        )

    def test_create_tweet(self):

        response = self.client.post("/api/v1/tweets/")
        self.assertEqual(
            response.status_code,
            403,
        )

        self.client.force_login(self.user)
        response = self.client.post("/api/v1/tweets/")
        self.assertEqual(
            response.status_code,
            400,
        )
        response = self.client.post(
            "/api/v1/tweets/",
            {
                "payload": "",
            },
        )
        self.assertEqual(
            response.status_code,
            400,
        )
        response = self.client.post(
            "/api/v1/tweets/",
            {
                "payload": self.CONTENT,
            },
        )
        data = response.json()
        self.assertEqual(
            response.status_code,
            200,
        )
        self.assertEqual(
            data["payload"],
            self.CONTENT,
        )
        self.assertEqual(data["user"]["pk"], self.user.pk)


class TestTweetDetailAPI(APITestCase):

    CONTENT = "testest"

    def setUp(self):
        owner = User.objects.create(
            username="owner",
        )
        owner.set_password("0000")
        owner.save()
        self.owner = owner

        non_owner = User.objects.create(
            username="non_owner",
        )
        non_owner.set_password("0000")
        non_owner.save()
        self.non_owner = non_owner

        Tweet.objects.create(
            user=self.owner,
            payload=self.CONTENT,
        )

    def test_get_tweet(self):

        response = self.client.get("/api/v1/tweets/9999")
        self.assertEqual(
            response.status_code,
            404,
        )

        response = self.client.get("/api/v1/tweets/1")
        data = response.json()
        self.assertEqual(
            response.status_code,
            200,
        )
        self.assertEqual(
            data["user"]["pk"],
            self.owner.pk,
        )
        self.assertEqual(
            data["payload"],
            self.CONTENT,
        )

    def test_put_tweet(self):
        response = self.client.put("/api/v1/tweets/1")
        self.assertEqual(
            response.status_code,
            403,
        )

        self.client.force_login(self.non_owner)
        response = self.client.put("/api/v1/tweets/9999")
        self.assertEqual(
            response.status_code,
            404,
        )
        response = self.client.put("/api/v1/tweets/1")
        self.assertEqual(
            response.status_code,
            403,
        )

        self.client.logout()
        self.client.force_login(self.owner)
        response = self.client.put("/api/v1/tweets/1")
        self.assertEqual(
            response.status_code,
            200,
        )
        response = self.client.put(
            "/api/v1/tweets/1",
            {
                "payload": "",
            },
        )
        self.assertEqual(
            response.status_code,
            400,
        )

    def test_delete_tweet(self):
        response = self.client.delete("/api/v1/tweets/1")
        self.assertEqual(
            response.status_code,
            403,
        )

        self.client.force_login(self.non_owner)
        response = self.client.delete("/api/v1/tweets/9999")
        self.assertEqual(
            response.status_code,
            404,
        )
        response = self.client.delete("/api/v1/tweets/1")
        self.assertEqual(
            response.status_code,
            403,
        )

        self.client.logout()
        self.client.force_login(self.owner)
        response = self.client.delete("/api/v1/tweets/1")
        self.assertEqual(
            response.status_code,
            204,
        )
        response = self.client.delete("/api/v1/tweets/1")
        self.assertEqual(
            response.status_code,
            404,
        )
