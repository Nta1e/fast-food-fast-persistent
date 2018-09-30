import unittest
import json
from app.models.models import drop, initialize
from app import app


class MenuTestCase(unittest.TestCase):

    def setUp(self):
        drop()
        initialize()
        self.client = app.test_client(self)
        self.data = {
            "admin": {
                "username": "Ntale",
                "email": "Ntale@andela.com",
                "password": "*****",
                "confirm_password": "*****",
                "role": "admin"
            },
            "login1": {
                "username": "Ntale",
                "password": "*****"
            },
            "user": {
                "username": "Grey",
                "email": "Grey@saint.com",
                "password": "#####",
                "confirm_password": "#####"
            },
            "login2": {
                "username": "Grey",
                "password": "#####"
            },
            "menu": {
                "menu_item": "3 Chicken wings",
                "price": 2000
            },
            "string": {
                "menu_item": "1 Chicken wing",
                "price": "1000"
            },
            "spaces": {
                "menu_item": " ",
                "price": 10000
            },
            "update": {
                "menu_item": "fish",
                "price": 2000
            }
        }
        # Admin signup and login to get access token
        self.client.post(
            'api/v2/auth/signup',
            data=json.dumps(
                self.data["admin"]),
            content_type='application/json')
        self.response = self.client.post('/api/v2/auth/login', data=json.dumps(
            self.data["login1"]), content_type='application/json')
        self.access_token = json.loads(self.response.data.decode())['token']
        self.auth_header = {
            'Authorization': 'Bearer {}'.format(self.access_token)}

        # Normal user signup and login to get access token
        self.client.post(
            'api/v2/auth/signup',
            data=json.dumps(
                self.data["user"]),
            content_type='application/json')
        self.response = self.client.post('/api/v2/auth/login', data=json.dumps(
            self.data["login2"]), content_type='application/json')
        self.access_token_2 = json.loads(self.response.data.decode())['token']
        self.auth_header_2 = {
            'Authorization': 'Bearer {}'.format(self.access_token_2)}

    def tearDown(self):
        drop()

    def test_invalid_content_type(self):
        '''
            This tests for the response when a wrong content_type is used in the body
        '''
        res = self.client.post(
            '/api/v2/admin/menu',
            data=json.dumps(
                self.data["menu"]),
            headers=self.auth_header,
            content_type='text/plain')
        self.assertEqual(res.status_code, 400)
        self.assertTrue(b'Invalid content_type', res.data)

    def test_admin_can_add_meal(self):
        '''This tests whether an admin user can add a meal option to the menu'''
        res = self.client.post(
            '/api/v2/admin/menu',
            data=json.dumps(
                self.data["menu"]),
            headers=self.auth_header,
            content_type='application/json')
        self.assertEqual(res.status_code, 201)
        self.assertTrue(b'New meal added!', res.data)

    def test_meal_cannot_be_added_twice(self):
        '''This tests whether a meal option cannot be added twice'''
        res = self.client.post(
            '/api/v2/admin/menu',
            data=json.dumps(
                self.data["menu"]),
            headers=self.auth_header,
            content_type='application/json')
        res = self.client.post(
            '/api/v2/admin/menu',
            data=json.dumps(
                self.data["menu"]),
            headers=self.auth_header,
            content_type='application/json')
        self.assertEqual(res.status_code, 409)
        self.assertTrue(b'Meal already exists!', res.data)

    def test_only_admin_can_add_meal(self):
        '''This tests whether only the admin can add a meal option'''
        res = self.client.post(
            '/api/v2/admin/menu',
            data=json.dumps(
                self.data["menu"]),
            headers=self.auth_header_2,
            content_type='application/json')
        self.assertEqual(res.status_code, 403)
        self.assertTrue(b'Admins only!', res.data)

    def test_price_cannot_be_a_string(self):
        '''This tests whether price cannot be a string'''
        res = self.client.post(
            '/api/v2/admin/menu',
            data=json.dumps(
                self.data["string"]),
            headers=self.auth_header,
            content_type='application/json')
        self.assertEqual(res.status_code, 400)
        self.assertTrue(b'Price has to be an integer', res.data)

    def test_cannot_add_meal_with_empty_spaces(self):
        '''This tests whether a meal cannot be added with spaces in input fields'''
        res = self.client.post(
            '/api/v2/admin/menu',
            data=json.dumps(
                self.data["spaces"]),
            headers=self.auth_header,
            content_type='application/json')
        self.assertEqual(res.status_code, 400)
        self.assertTrue(b'Required field/s missing', res.data)

    def test_admin_can_edit_menu(self):
        '''This tests whether the admin can update the menu'''
        res = self.client.post(
            '/api/v2/admin/menu',
            data=json.dumps(
                self.data["menu"]),
            headers=self.auth_header,
            content_type='application/json')
        res = self.client.put(
            '/api/v2/admin/menu/1',
            data=json.dumps(
                self.data["update"]),
            headers=self.auth_header,
            content_type='application/json')
        self.assertEqual(res.status_code, 201)
        self.assertTrue(b'Menu updated!', res.data)

    def test_cannot_edit_unavailable_meal(self):
        """This tests whether the admin cannot edit a meal that doesnot exist"""
        res = self.client.post(
            '/api/v2/admin/menu',
            data=json.dumps(
                self.data["menu"]),
            headers=self.auth_header,
            content_type='application/json')
        res = self.client.put(
            '/api/v2/admin/menu/3',
            data=json.dumps(
                self.data["update"]),
            headers=self.auth_header,
            content_type='application/json')
        self.assertEqual(res.status_code, 404)

    def test_admin_can_delete_meal_option(self):
        '''This tests whether the admin can delete a meal option'''
        res = self.client.post(
            '/api/v2/admin/menu',
            data=json.dumps(
                self.data["menu"]),
            headers=self.auth_header,
            content_type='application/json')
        res = self.client.delete(
            '/api/v2/admin/menu/1',
            headers=self.auth_header,
            content_type='application/json')
        self.assertTrue(res.status_code, 200)

    def test_cannot_delete_unavailable_meal(self):
        '''This tests whether admin cannot delete a meal tha doesnot exist'''
        res = self.client.post(
            '/api/v2/admin/menu',
            data=json.dumps(
                self.data["menu"]),
            headers=self.auth_header,
            content_type='application/json')
        res = self.client.delete(
            '/api/v2/admin/menu/5',
            headers=self.auth_header,
            content_type='application/json')
        self.assertTrue(res.status_code, 404)

    def test_user_can_view_menu(self):
        '''This tests whether a user can view the available menu'''
        res = self.client.get(
            '/api/v2/users/menu',
            headers=self.auth_header_2,
            content_type='application/json')
        self.assertEqual(res.status_code, 200)
