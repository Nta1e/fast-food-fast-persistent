# Fast-Food-Fast API
[![Build Status](https://travis-ci.org/NtaleShadik/fast-food-fast-c3.svg?branch=ft-update_order_160787812)](https://travis-ci.org/NtaleShadik/fast-food-fast-c3)
[![Coverage Status](https://coveralls.io/repos/github/NtaleShadik/fast-food-fast-c3/badge.svg?branch=ft-update_order_160787812)](https://coveralls.io/github/NtaleShadik/fast-food-fast-c3?branch=ft-update_order_160787812)
[![Open Source Love](https://badges.frapsoft.com/os/v2/open-source.svg?v=103)](https://github.com/ellerbrock/open-source-badges/)
## Description
Fast-Food-Fast is a food delivery service app for a restaurant.

## The project has the following routes

| REQUEST | ROUTE | FUNCTIONALITY |
| ------- | ----- | ------------- |
| *POST* | ```/api/v2/auth/signup``` | _Register new user_|
| *POST* | ```/api/v2/auth/login``` | _user login_|
| *GET* | ```/api/v2/admin/users``` | _view all users_|
| *POST* | ```/api/v2/admin/menu``` | _Add meal to menu_
| *PUT* | ```/api/v2/admin/menu/<meal_id>``` | _Edit menu_|
| *DELETE* | ```/api/v2/admin/menu/<meal_id>/delete``` | _Delete meal_|
| *GET* | ```/api/v2/users/menu``` | _view menu_|
| *POST* | ```/api/v2/users/orders``` | _place an order for food_|
| *GET* | ```/api/v2/users/orders``` | _Get user orders_|
| *GET* | ```/api/v2/admin/orders``` | _Get all orders_|
| *GET* | ```/api/v2/admin/orders/<order_id>``` | _Get one order_|
| *PUT* | ```/api/v2/admin/orders/<order_id>``` | _Update order status_|

