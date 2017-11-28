from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from django.test import Client
from osschallenge.tests.pages.register import RegisterPage
from osschallenge.models import User


class MydriverTests(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(self):
        super(MydriverTests, self).setUpClass()
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1200x600')
        self.driver = webdriver.Chrome(chrome_options=options)
        self.driver.implicitly_wait(10)

    @classmethod
    def setUp(self):
        self.client = Client()
        self.register_page = RegisterPage(self.driver, self.live_server_url)

    @classmethod
    def tearDownClass(self):
        self.driver.quit()
        super(MydriverTests, self).tearDownClass()

    def test_register_successful(self):
        self.register_page.open()
        self.register_page.register(
            "myuser",
            "foo",
            "bar",
            "example@example.ch",
            "12345qwert",
            "12345qwert"
        )
        user = User.objects.get(username="myuser")
        self.assertEqual(user.username, "myuser")
        self.assertEqual(user.first_name, "foo")
        self.assertEqual(user.last_name, "bar")
        self.assertEqual(user.email, "example@example.ch")

    def test_register_name_already_taken(self):
        self.register_page.open()
        self.register_page.register(
            "Test",
            "foo",
            "bar",
            "example@example.ch",
            "12345qwert",
            "12345qwert"
        )
        self.assertRaises(AssertionError)

    def test_register_passwords_do_not_match(self):
        self.register_page.open()
        self.register_page.register(
            "Test",
            "foo",
            "bar",
            "example@example.ch",
            "12345qwert",
            "qwert12345"
        )
        self.assertRaises(AssertionError)
