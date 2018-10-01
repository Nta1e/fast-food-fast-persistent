import unittest
import json
from app.models.models import drop, initialize
from app import app


class OrdersTestCase(unittest.TestCase):

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
            "order": {
                "order": "3 Chicken wings",
                "location": "kamwokya",
                "comment": "give me my money's worth"
            },
            "wrong_order": {
                "order": "fish",
                "location": "Ntinda",
                "comment": "give me my money's worth"
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

    def test_user_can_make_an_order(self):
        '''This tests whether a user can place an order for food'''
        res = self.client.post('api/v2/admin/menu', data=json.dumps(
            self.data["menu"]), headers=self.auth_header, content_type='application/json')
        res = self.client.post('api/v2/users/orders', data=json.dumps(
            self.data["order"]), headers=self.auth_header_2, content_type='application/json')
        self.assertEqual(res.status_code, 201)

    def test_user_cannot_make_order_for_non_existing_meal(self):
        '''This tests whether a user cannot make an order for a meal that doesnot exist on the menu'''
        res = self.client.post('api/v2/users/orders', data=json.dumps(
            self.data["wrong_order"]), headers=self.auth_header_2, content_type='application/json')
        self.assertEqual(res.status_code, 400)

    def test_user_can_get_his_orders(self):
        '''This tests whether the user can get all the orders made by him'''
        res = self.client.get(
            'api/v2/users/orders', headers=self.auth_header_2, content_type='application/json')
        self.assertEqual(res.status_code, 200)
