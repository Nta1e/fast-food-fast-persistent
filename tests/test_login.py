import json
import unittest

from app import app
from app.models.models import drop, initialize


class LoginTestCase(unittest.TestCase):

    def setUp(self):
        drop()
        initialize()
        self.client = app.test_client(self)
        self.data = {
            "user": {
                "username": "West",
                "email": "kanye@west.com",
                "password": "pie123",
                "confirm_password": "pie123"
            },
            "login": {
                "username": "West",
                "password": "pie123"
            },
            "wrong_password": {
                "username": "West",
                "password": "pie245"
            },
            "unknown": {
                "username": "Jamie",
                "password": "shhhhh"
            }
        }

    def tearDown(self):
        drop()

    def test_user_can_login(self):
        '''This tests whether a registered user can login'''
        res = self.client.post(
            '/api/v2/auth/signup', data=json.dumps(self.data["user"]),
            content_type='application/json')
        res = self.client.post(
            '/api/v2/auth/login', data=json.dumps(self.data["login"]),
            content_type='application/json')
        self.assertEqual(res.status_code, 200)
        self.assertTrue(b'Login successfull!', res.data)

    def test_wrong_password(self):
        '''This tests whether a user cannot login with a wrong password'''
        res = self.client.post(
            '/api/v2/auth/signup', data=json.dumps(self.data["user"]),
            content_type='application/json')
        res = self.client.post(
            '/api/v2/auth/login', data=json.dumps(self.data["wrong_password"]),
            content_type='application/json')
        self.assertEqual(res.status_code, 401)
        self.assertTrue(b'password incorrect!', res.data)

    def test_unknown_user_cannot_login(self):
        '''This tests whether an unknown user cannot login'''
        res = self.client.post(
            '/api/v2/auth/login', data=json.dumps(self.data["unknown"]),
            content_type='application/json')
        self.assertEqual(res.status_code, 400)
        self.assertTrue(b'User does not exist!', res.data)
