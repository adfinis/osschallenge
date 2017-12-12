from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from osschallenge.tests.pages.ranking import RankingPage
from django.test import Client


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
        self.ranking_page = RankingPage(self.driver, self.live_server_url)
        self.client = Client()

    @classmethod
    def tearDownClass(self):
        self.driver.quit()
        super(MydriverTests, self).tearDownClass()

    def test_ranking_with_no_users(self):
        self.ranking_page.open('/ranking/?page=100')
        message = self.ranking_page.find_message()
        self.assertEquals(message.text, 'No users available')
