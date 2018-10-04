# Fast-Food-Fast API
[![Build Status](https://travis-ci.org/NtaleShadik/fast-food-fast-c3.svg?branch=develop)](https://travis-ci.org/NtaleShadik/fast-food-fast-c3)
[![Coverage Status](https://coveralls.io/repos/github/NtaleShadik/fast-food-fast-c3/badge.svg?branch=develop)](https://coveralls.io/github/NtaleShadik/fast-food-fast-c3?branch=develop)
[![Maintainability](https://api.codeclimate.com/v1/badges/7646572a208b37bf453d/maintainability)](https://codeclimate.com/github/NtaleShadik/fast-food-fast-c3/maintainability)
[![Open Source Love](https://badges.frapsoft.com/os/v2/open-source.svg?v=103)](https://github.com/ellerbrock/open-source-badges/)
## Description
Fast-Food-Fast is a food delivery service app for a restaurant.
The documentation of the API can be found [here](https://v2-fastfoodfast.herokuapp.com)

## The project has the following routes

| REQUEST | ROUTE | FUNCTIONALITY |
| ------- | ----- | ------------- |
| *POST* | ```/api/v2/auth/signup``` | _Register new user_|
| *POST* | ```/api/v2/auth/login``` | _user login_|
| *GET* | ```/api/v2/admin/users``` | _view all users_|
| *POST* | ```/api/v2/admin/menu``` | _Add meal to menu_|
| *PUT* | ```/api/v2/admin/menu/<meal_id>``` | _Edit menu_|
| *DELETE* | ```/api/v2/admin/menu/<meal_id>/delete``` | _Delete meal_ |
| *GET* | ```/api/v2/users/menu``` | _view menu_|
| *POST* | ```/api/v2/users/orders``` | _place an order for food_|
| *GET* | ```/api/v2/users/orders``` | _Get user orders_|
| *GET* | ```/api/v2/admin/orders``` | _Get all orders_|
| *GET* | ```/api/v2/admin/orders/<order_id>``` | _Get one order_|
| *PUT* | ```/api/v2/admin/orders/<order_id>``` | _Update order status_|

## BUILT WITH

* Flask - Python Framework used

## SETTING UP APPLICATION
1. Install postgresql

2. Create a folder Fast-food-fast

    Clone repository to the folder

    **```git clone https://github.com/NtaleShadik/Fast-food-fast-c3.git```**

3. Create a virtual environment that you are going to use while running the application locally

    **```$ python3 -m venv env```**

    **```$ source  env/bin/activate```**

4. Install all project dependencies using

    **```pip3 install -r requirements.txt```**

5. Tweak the ```database.py``` file in the models folder to suit your connection credentials

6. Run the appliction from the root of your folder using

    **```python3 run.py```**

## Author

*Ntale Shadik*


