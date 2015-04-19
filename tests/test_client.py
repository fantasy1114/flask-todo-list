# -*- coding: utf-8 -*-

from flask.ext.testing import TestCase

from flask import url_for

from app import create_app, db
from app.models import  User, Todo


class TodolistClientTestCase(TestCase):

    def create_app(self):
        return create_app('testing')

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def register_user(self, name):
        response = self.client.post(url_for('auth.register'), data={
            'username': name,
            'email': name +'@example.com',
            'password': 'correcthorsebatterystaple',
            'password_confirmation': 'correcthorsebatterystaple'
        })
        return response

    def login_user(self, name):
        response = self.client.post(url_for('auth.login'), data={
            'email_or_username': name + '@example.com',
            'password': 'correcthorsebatterystaple'
        })
        return response

    def register_and_login(self, name):
        response = self.register_user(name)
        self.assert_redirects (response, '/auth/login')
        response = self.login_user(name)
        self.assert_redirects (response, '/')

    def test_home_page(self):
        response = self.client.get(url_for('main.index'))
        self.assert_200(response)
        self.assert_template_used('index.html')

    def test_register_page(self):
        response = self.client.get(url_for('auth.register'))
        self.assert_200(response)
        self.assert_template_used('register.html')

    def test_login_page(self):
        response = self.client.get(url_for('auth.login'))
        self.assert_200(response)
        self.assert_template_used('login.html')

    def test_overview_page(self):
        self.register_and_login('adam')
        response = self.client.get(url_for('main.todolist_overview'))
        # expect not redirect as user is logged in
        self.assert_200(response)
        self.assert_template_used('overview.html')

    def test_last_seen_update_after_login(self):
        response = self.register_user('adam')
        before = User.query.filter_by(username='adam').first().last_seen
        response = self.login_user('adam')
        after = User.query.filter_by(username='adam').first().last_seen
        self.assertNotEqual(before, after)

    def test_register_and_login_and_logout(self):
        # register a new account
        response = self.register_user('adam')
        # expect redirect to login
        self.assert_redirects (response, '/auth/login')

        # login with the new account
        response = self.login_user('adam')
        # expect redirect to index
        self.assert_redirects (response, '/')

        # logout
        response = self.client.get(url_for('auth.logout'),
                                   follow_redirects=True)
        # follow redirect to index
        self.assert_200(response)
        self.assert_template_used('index.html')
