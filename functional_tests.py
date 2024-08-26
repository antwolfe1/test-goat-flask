import time
import unittest

from Tools.scripts.generate_opcode_h import header
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By


class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

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
        # "1: Buy peacock feathers" as an item in a to-do list
        box.send_keys(Keys.ENTER)
        time.sleep(1)

        table = self.browser.find_element(By.ID, "id_list_table")
        rows = table.find_elements(By.TAG_NAME, "tr")
        self.assertTrue(any(row.text == "1: Buy peacock feathers" for row in rows), "New to-do item did not appear in table")

        # There is still a text box inviting her to add another item.
        # She enters "Use peacock feathers to make a fly" (Edith is very methodical)
        self.fail("Finish the test!")

        # The page updates again, and now shows both items on her list

        # Satisfied, she goes back to sleep


if __name__ == "__main__":
    unittest.main()
