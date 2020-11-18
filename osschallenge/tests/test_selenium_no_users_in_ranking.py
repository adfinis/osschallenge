from osschallenge.tests.pages.ranking import RankingPage
from osschallenge.tests.pages.login import LoginPage
from django.test import Client
from osschallenge.tests.selenium_test_options import SeleniumTests
from . import factories
from django.contrib.auth.models import Group
from osschallenge.models import Rank


class NoUsersInRankingTest(SeleniumTests):

    @classmethod
    def setUpClass(self):
        super(NoUsersInRankingTest, self).setUpClass()

    @classmethod
    def setUp(self):
        self.client = Client()
        self.ranking_page = RankingPage(self.driver, self.live_server_url)
        self.login_page = LoginPage(self.driver, self.live_server_url)
        self.rank2 = Rank.objects.create(
            id=2,
            name="Youngling",
            required_points=15
        )
        self.user1 = factories.UserFactory(username="Test")
        self.user1.set_password("12345qwert")
        self.user1.save()
        self.group2 = Group.objects.create(
            id = 1,
            name = "Mentor"
        )
        self.login_page.open()
        self.login_page.login("Test", "12345qwert")
        self.client.login(username="Test", password='klajsdfkj')
        self.driver.get(self.live_server_url + '/login/')

    @classmethod
    def tearDownClass(self):
        self.driver.quit()
        super(NoUsersInRankingTest, self).tearDownClass()

    def test_ranking_with_no_users(self):
        self.ranking_page.open('/ranking/?page=100')
        self.group2.user_set.add(self.user1)
        message = self.ranking_page.find_message()
        self.assertEquals(message.text, 'No users available')
