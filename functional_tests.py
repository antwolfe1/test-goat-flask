import tempfile
import time
import unittest

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

from app import app, db


class NewVisitorTest(unittest.TestCase):

    db_fd, db_path = tempfile.mkstemp()
    SQLALCHEMY_DATABASE_URI = "sqlite:///"
    TESTING = True

    def setUp(self):
        self.browser = webdriver.Chrome()
        with app.test_request_context():
            db.create_all()

    def tearDown(self):
        self.browser.quit()
        with app.test_request_context():
            db.session.remove()
            db.drop_all()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element(By.ID, "id_list_table")
        rows = table.find_elements(By.TAG_NAME, "tr")
        self.assertIn(row_text, [row.text for row in rows],
                      f"New to-do item did not appear in table. Contents were: \n{table.text}")

    def test_can_start_a_todo_list(self):
        # Edith has heard about a cool new online to-do app.
        # She goes to check out its homepage
        self.browser.get("http://localhost:5000")

        # She notices the page title and header mention to-do lists
        self.assertIn("To-Do", self.browser.title)
        header = self.browser.find_element(By.TAG_NAME, "h1").text
        self.assertIn("To-Do", header)

        # She is invited to enter a to-do item straight away
        box = self.browser.find_element(By.ID, "id_new_item")
        self.assertEqual(box.get_attribute("placeholder"), "enter a to-do item")

        # She types "Buy peacock feathers" into a text box
        # (Edith's hobby is tying fly-fishing lures)
        box.send_keys("Buy peacock feathers")

        # When she hits enter, the page updates, and now the page lists
        box.send_keys(Keys.ENTER)
        time.sleep(1)

        # "1: Buy peacock feathers" as an item in a to-do list
        self.check_for_row_in_list_table("1: Buy peacock feathers")

        # There is still a text box inviting her to add another item.
        # She enters "Use peacock feathers to make a fly" (Edith is very methodical)
        box = self.browser.find_element(By.ID, "id_new_item")
        box.send_keys("Use peacock feathers to make a fly")
        box.send_keys(Keys.ENTER)
        time.sleep(1)

        # The page updates again, and now shows both items on her list
        self.check_for_row_in_list_table("1: Buy peacock feathers")
        self.check_for_row_in_list_table("2: Use peacock feathers to make a fly")

        # Satisfied, she goes back to sleep
        self.fail("Finish the test!")


if __name__ == "__main__":
    unittest.main()
