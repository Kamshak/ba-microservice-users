# coding: utf-8
from behave import given, when, then
import json
import sys
import requests
import datetime
from hamcrest import assert_that, equal_to, has_key, instance_of
from user_service.models import User


HOST = 'http://localhost:5000'


@given("Flask app is running")
def start_app(context):
    response = requests.get(HOST)
    assert response.status_code == 200


@when("We save a user")
def save_user(context):
    user = {'first_name': 'First',
            'last_name': 'Last',
            'birth_date': datetime.date.today().isoformat(),
            'email': 'test@email.com',
            'password': 'password',
            'phone': '48888'}

    json_user = json.dumps(user)
    headers = {'content-type': 'application/json'}
    response = requests.post(HOST+'/api/users', data=json_user, headers=headers)
    context.last_user_id = response.json()['id']
    assert_that(response.status_code, equal_to(201))

@given("We have an user")
def we_have_an_user(context):
    user = {'first_name': 'First',
            'last_name': 'Last',
            'birth_date': datetime.date.today().isoformat(),
            'email': 'test2@email.com',
            'password': 'password',
            'phone': '48888'}

    json_user = json.dumps(user)
    headers = {'content-type': 'application/json'}
    response = requests.post(HOST+'/api/users', data=json_user, headers=headers)
    context.last_user_id = response.json()['id']
    assert_that(response.status_code, equal_to(201))


@then("The user exists")
def find_user(context):
    user = User.query.filter_by(first_name="First", last_name="Last", email="test@email.com", password="password").first()
    assert_that(user, instance_of(User))

@given("We are logged in")
def we_are_logged_in(context):
    user = {'username': 'test2@email.com',
            'password': 'password'}

    json_user = json.dumps(user)
    headers = {'content-type': 'application/json'}
    response = requests.post(HOST+'/auth', data=json_user, headers=headers)
    assert_that(response.status_code, equal_to(200))
    assert_that(response.json(), has_key('access_token'))
    context.access_token = response.json()["access_token"]

@when("We update the user")
def update_user(context):
    user = {'id': context.last_user_id,
            'first_name': 'UpdatedFirst',
            'last_name': 'Last',
            'birth_date': datetime.date.today().isoformat(),
            'email': 'test2@email.com',
            'password': 'password',
            'phone': '48888'}

    json_user = json.dumps(user)
    headers = {'content-type': 'application/json', 'Authorization': 'JWT ' + context.access_token}
    response = requests.put(HOST+'/api/users/'+context.last_user_id, data=json_user, headers=headers)

    assert_that(response.status_code, equal_to(200))


@then("The user is updated")
def check_update(context):
    headers = {'content-type': 'application/json', 'Authorization': 'JWT ' + context.access_token}
    response = requests.get(HOST+'/api/users/'+context.last_user_id, headers=headers)
    assert_that(response.status_code, equal_to(200))
    assert_that(response.json()['first_name'], equal_to('UpdatedFirst'))


@when("Submit login data")
def login_user(context):
    user = {'username': 'test2@email.com',
            'password': 'password'}

    json_user = json.dumps(user)
    headers = {'content-type': 'application/json'}
    response = requests.post(HOST+'/auth', data=json_user, headers=headers)
    context.response = response


@then("JWT is returned")
def check_login(context):
    assert_that(context.response.status_code, equal_to(200))
    assert_that(context.response.json(), has_key('access_token'))

@when("We request our user")
def request_user(context):
    headers = {'content-type': 'application/json', 'Authorization': 'JWT ' + context.access_token}
    response = requests.get(HOST+'/api/users/'+context.last_user_id, headers=headers)
    context.response = response

@then("The email is returned")
def email_returned(context):
    assert_that(context.response.status_code, equal_to(200))
    assert_that(context.response.json(), has_key('email'))
