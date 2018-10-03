import unittest
import json
from app.models.models import drop, initialize
from app import app


class RegistrationTestCase(unittest.TestCase):

    def setUp(self):
        drop()
        initialize()
        self.client = app.test_client(self)
        self.data = {
            "admin": {
                "username": "Grey",
                "email": "Grey@admin.com",
                "password": "Sean123",
                "confirm_password": "Sean123",
                "role": "admin"
            },
            "user": {
                "username": "West",
                "email": "kanye@west.com",
                "password": "pie123",
                "confirm_password": "pie123"
            },
            "user2": {
                "username": "Pusha",
                "email": "kanye@west.com",
                "password": "pie123",
                "confirm_password": "pie123"
            },
            "spaces": {
                "username": " ",
                "email": "you@me.com",
                "password": "password",
                "confirm_password": "password"
            },
            "mismatch": {
                "username": "Seandon",
                "email": "sean@andela.com",
                "password": "sean#don",
                "confirm_password": "sean*don"
            },
            "invalid_email": {
                "username": "St.patrick",
                "email": "Stpatrick.com",
                "password": "pie123",
                "confirm_password": "pie123"
            },
            "missing_fields": {
                "username": "",
                "email": "",
                "password": "pie123",
                "confirm_password": "pie123"
            },
            "short": {
                "username": "Pie",
                "email": "pie@123.com",
                "password": "pie",
                "confirm_password": "pie"
            }

        }

    def tearDown(self):
        drop()

    def test_admin_can_register(self):
        '''This tests whether an admin user can register'''
        res = self.client.post(
            '/api/v2/auth/signup',
            data=json.dumps(
                self.data["admin"]),
            content_type='application/json')
        self.assertEqual(res.status_code, 201)
        self.assertTrue(b'Registration Successfull', res.data)

    def test_normal_user_can_register(self):
        '''This tests whether a normal user can register'''
        res = self.client.post(
            '/api/v2/auth/signup',
            data=json.dumps(
                self.data["user"]),
            content_type='application/json')
        self.assertEqual(res.status_code, 201)
        self.assertTrue(b'Registration Successfull', res.data)

    def test_user_cannot_signup_twice(self):
        '''This tests whether a user cannot register with the same credentials twice'''
        res = self.client.post(
            '/api/v2/auth/signup',
            data=json.dumps(
                self.data["user"]),
            content_type='application/json')
        res = self.client.post(
            '/api/v2/auth/signup',
            data=json.dumps(
                self.data["user"]),
            content_type='application/json')
        self.assertEqual(res.status_code, 409)

    def test_user_cannot_register_with_empty_spaces(self):
        '''This tests whether a user cannot register with empty spaces in required fields'''
        res = self.client.post(
            '/api/v2/auth/signup',
            data=json.dumps(
                self.data["spaces"]),
            content_type='application/json')
        self.assertEqual(res.status_code, 400)
        self.assertTrue(b'Required field/s Missing', res.data)

    def test_user_cannot_register_with_missing_fields(self):
        '''This tests whether a user cannot register with missing fields'''
        res = self.client.post(
            '/api/v2/auth/signup',
            data=json.dumps(
                self.data["missing_fields"]),
            content_type='application/json')
        self.assertEqual(res.status_code, 400)
        self.assertTrue(b'Required field/s Missing', res.data)

    def test_password_mismatch(self):
        '''This tests whether a user cannot register with unmatching passwords'''
        res = self.client.post(
            '/api/v2/auth/signup',
            data=json.dumps(
                self.data["mismatch"]),
            content_type='application/json')
        self.assertEqual(res.status_code, 400)
        self.assertTrue(b'Your passwords do not match!', res.data)

    def test_invalid_email(self):
        '''This tests whether a user cannot register with an invalid email'''
        res = self.client.post(
            '/api/v2/auth/signup',
            data=json.dumps(
                self.data["invalid_email"]),
            content_type='application/json')
        self.assertEqual(res.status_code, 400)
        self.assertTrue(b'Invalid email', res.data)

    def test_short_password(self):
        '''This tests whether a user cannot register with a short password'''
        res = self.client.post(
            '/api/v2/auth/signup',
            data=json.dumps(
                self.data["short"]),
            content_type='application/json')
        self.assertEqual(res.status_code, 400)
        self.assertTrue(b'Password too short!', res.data)

    def test_user_cannot_register_with_existing_email(self):
        '''This tests whether a user cannot register with an already existing email'''
        res = self.client.post(
            '/api/v2/auth/signup',
            data=json.dumps(
                self.data["user"]),
            content_type='application/json')
        res = self.client.post(
            '/api/v2/auth/signup',
            data=json.dumps(
                self.data["user2"]),
            content_type='application/json')
        self.assertEqual(res.status_code, 409)
        self.assertTrue(b'Email already exists!', res.data)

    def test_invalid_content_type(self):
        '''
        This tests for the response when a wrong content_type is used in the body
        '''
        res = self.client.post(
            '/api/v2/auth/signup',
            data=json.dumps(
                self.data["user"]),
            content_type='text/plain')
        self.assertEqual(res.status_code, 400)
        self.assertTrue(b'Invalid content_type', res.data)
