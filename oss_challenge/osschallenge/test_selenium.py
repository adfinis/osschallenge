from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver


class MySeleniumTests(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super(MySeleniumTests, cls).setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(MySeleniumTests, cls).tearDownClass()

    def test_login(self):
        self.selenium.get('{}{}'.format(self.live_server_url, '/login/'))
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys('myuser')
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys('secret')
        self.selenium.find_element_by_xpath('//button[@value="login"]').click()

    def test_login_and_go_to_mytasks(self):
        self.selenium.get('{}{}'.format(self.live_server_url, '/login/'))
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys('Yelin')
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys('12345qwert')
        self.selenium.find_element_by_xpath('//button[@value="login"]').click()
        self.selenium.get(
            '{}{}'.format(self.live_server_url, '/my_tasks/Yelin/')
        )
