import tempfile
from unittest import TestCase

from app import app, db, Item



class HomePageTest(TestCase):
    db_fd, db_path = tempfile.mkstemp()
    SQLALCHEMY_DATABASE_URI = "sqlite:///"
    TESTING = True

    def setUp(self):
        self.test_app = app.test_client(self)
        with app.test_request_context():
            db.create_all()

    def tearDown(self):
        with app.test_request_context():
            db.session.remove()
            db.drop_all()

    def test_home_page_returns_correct_html(self):
        response = self.test_app.get('/')
        html = response.get_data(as_text=True)
        self.assertIn("<title>To-Do lists</title>", html)
        self.assertIn("<html>", html)
        self.assertIn("</html>", html)

    def test_displays_all_list_items(self):
        with app.test_request_context():
            Item().delete_all()
            Item().text = "itemey 1"
            Item().text = "itemey 2"
            response = self.test_app.get("/")
        self.assertIn(response.get_data(as_text=True), "itemey 1")
        self.assertIn(response.get_data(as_text=True), "itemey 2")

    def test_can_save_a_POST_request(self):
        response = self.test_app.post("/", data={"item_text": "A new list item"})

        self.assertEqual(Item.query.count(), 1)
        new_item = Item.query.first()
        self.assertEqual(new_item.text, "A new list item")
        self.assertIn("A new list item", response)

    def test_only_saves_item_when_necessary(self):
        self.test_app.get("/")
        self.assertEqual(Item.query.count(), 0)


class ItemModelTest(TestCase):
    db_fd, db_path = tempfile.mkstemp()
    SQLALCHEMY_DATABASE_URI = "sqlite:///"
    TESTING = True

    def setUp(self):
        app.testing = True
        with app.test_request_context():
            db.create_all()

    def tearDown(self):
        with app.test_request_context():
            db.session.remove()
            db.drop_all()

    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = "The first (ever) list item"
        first_item.save()

        second_item = Item()
        second_item.text = "The second list item"
        second_item.save()

        saved_items = Item.query.all()
        self.assertEqual(Item.query.count(), 2)  # rowcount

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, "The first (ever) list item")
        self.assertEqual(second_saved_item.text, "The second list item")
