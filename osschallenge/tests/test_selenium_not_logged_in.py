from django.test import Client
from osschallenge.tests.pages.register import RegisterPage
from osschallenge.tests.pages.rankup import RankUpPage
from osschallenge.tests.pages.profil import ProfilePage
from osschallenge.models import User, Rank
from osschallenge.tests.selenium_test_options import SeleniumTests
from . import factories
from django.contrib.auth.models import Group


class NotLoggedInTest(SeleniumTests):

    @classmethod
    def setUpClass(self):
        super(NotLoggedInTest, self).setUpClass()

    @classmethod
    def setUp(self):
        self.client = Client()
        self.register_page = RegisterPage(self.driver, self.live_server_url)
        self.rankup_page = RankUpPage(self.driver, self.live_server_url)
        self.profile_page = ProfilePage(self.driver, self.live_server_url)

        self.group1 = Group.objects.create(
            id=1,
            name="Contributor"
        )

        self.rank1 = Rank.objects.create(
            id=2,
            name="Padawan",
            required_points=15
        )

        self.user1 = factories.UserFactory(
            username="Test",
            email="example@example.ch"
        )
        self.user1.set_password("12345qwert")
        self.user1.save()
        self.group1.user_set.add(self.user1)

        self.profile1 = factories.ProfileFactory(
            user=self.user1,
            rank=self.rank1,
        )

    @classmethod
    def tearDownClass(self):
        self.driver.quit()
        super(NotLoggedInTest, self).tearDownClass()

    def test_register_successful(self):
        self.register_page.open()
        self.register_page.register(
            "myuser",
            "foo",
            "bar",
            "abc@example.ch",
            "12345qwert",
            "12345qwert"
        )
        user = User.objects.get(username="myuser")
        self.assertEqual(user.username, "myuser")
        self.assertEqual(user.first_name, "foo")
        self.assertEqual(user.last_name, "bar")
        self.assertEqual(user.email, "abc@example.ch")

    def test_register_name_already_taken(self):
        self.register_page.open()
        self.register_page.register(
            "Test",
            "foo",
            "bar",
            "abc@example.ch",
            "12345qwert",
            "12345qwert"
        )
        self.assertRaises(AssertionError)

    def test_register_email_already_taken(self):
        self.register_page.open()
        self.register_page.register(
            "myuser",
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
            "myuser",
            "foo",
            "bar",
            "example@example.ch",
            "12345qwert",
            "qwert12345"
        )
        self.assertRaises(AssertionError)

    def test_rankup_not_logged_in(self):
        self.rankup_page.open()
        element = self.rankup_page.search_element("form-control")
        self.assertTrue(element)

    def test_redirection_from_profile(self):
        self.profile_page.open("Test")
        element = self.profile_page.search_element('login')
        self.assertTrue(element)
