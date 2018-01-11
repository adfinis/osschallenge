from osschallenge.tests.pages.ranking import RankingPage
from django.test import Client
from osschallenge.tests.selenium_test_options import SeleniumTests


class NoUsersInRankingTest(SeleniumTests):

    @classmethod
    def setUpClass(self):
        super(NoUsersInRankingTest, self).setUpClass()

    @classmethod
    def setUp(self):
        self.ranking_page = RankingPage(self.driver, self.live_server_url)
        self.client = Client()

    @classmethod
    def tearDownClass(self):
        self.driver.quit()
        super(NoUsersInRankingTest, self).tearDownClass()

    def test_ranking_with_no_users(self):
        self.ranking_page.open('/ranking/?page=100')
        message = self.ranking_page.find_message()
        self.assertEquals(message.text, 'No users available')
