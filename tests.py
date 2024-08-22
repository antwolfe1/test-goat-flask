from unittest import TestCase

from flask import request

from main import app

class HomePageTest(TestCase):
    def test_home_page_returns_correct_html(self):
        test_app = app.test_client(self)
        response = test_app.get('/')
        html = response.get_data(as_text=True)
        # assert ("<title>To-Do</title>" in response.get_data(as_text=True), f"Home Page Title is: {response} ")
        self.assertIn("<title>To-Do lists</title>", html)