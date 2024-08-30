from unittest import TestCase


from main import app, Item


class HomePageTest(TestCase):
    def __init__(self, methodName: str = "runTest"):
        super().__init__(methodName)
        self.test_app = None

    def setUp(self):
        self.test_app = app.test_client(self)

    def test_home_page_returns_correct_html(self):
        response = self.test_app.get('/')
        html = response.get_data(as_text=True)
        self.assertIn("<title>To-Do lists</title>", html)
        self.assertIn("<html>", html)
        self.assertIn("</html>", html)

    def test_can_save_a_POST_request(self):
        response = self.test_app.post("/", data={"item_text": "A new list item"})
        self.assertIn("A new list item", response.get_data(as_text=True))



class ItemModelTest(TestCase):
    def test_saving_and_retrieving_items(self):

            first_item = Item()
            first_item.text = "The first (ever) list item"
            first_item.save()

            second_item = Item()
            second_item.text = "The second list item"
            second_item.save()

            saved_items = Item().all()
            self.assertEqual(saved_items.count(), 2) #rowcount

            first_saved_item = saved_items[0]
            second_saved_item = saved_items[1]
            self.assertEqual(first_saved_item.text, "The first (ever) list item")
            self.assertEqual(second_saved_item.text, "The second list item")
