from unittest import TestCase

from app import app, db, Item


class HomePageTest(TestCase):
    def __init__(self, methodName: str = "runTest"):
        super().__init__(methodName)
        self.test_app = None

    def setUp(self):
        app.testing = True
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
            Item(text = "itemey 1").save()
            Item(text = "itemey 2").save()
            response = self.test_app.get("/")
            print(response.get_data())
        self.assertIn("itemey 1", response.get_data(as_text=True))
        self.assertIn("itemey 2", response.get_data(as_text=True))


    def test_can_save_a_POST_request(self):
        with app.test_request_context():
            Item().delete_all()

            response = self.test_app.post("/", data={"item_text": "A new list item"})

            self.assertEqual(Item.query.count(), 1)
            new_item = Item.query.first()
            self.assertEqual(new_item.text, "A new list item")


    def test_only_saves_item_when_necessary(self):
        with app.test_request_context():
            Item().delete_all()
            self.test_app.get("/")
            self.assertEqual(Item.query.count(), 0)



class ItemModelTest(TestCase):

    def setUp(self):
        app.testing = True
        with app.test_request_context():
            db.create_all()

    def tearDown(self):
        with app.test_request_context():
            db.session.remove()
            db.drop_all()

    def test_saving_and_retrieving_items(self):
        with app.test_request_context():
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
