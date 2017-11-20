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

    def test_login_failed(self):
        self.selenium.get('{}{}'.format(self.live_server_url, '/login/'))
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys('myuser')
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys('secret')
        self.selenium.find_element_by_xpath('//button[@id="login"]').click()

    def test_login_and_go_to_mytasks(self):
        self.selenium.get('{}{}'.format(self.live_server_url, '/login/'))
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys('Yelin')
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys('12345qwert')
        self.selenium.find_element_by_xpath('//button[@id="login"]').click()
        self.selenium.get(
            '{}{}'.format(self.live_server_url, '/my_tasks/Yelin/')
        )

    def test_register(self):
        self.selenium.get('{}{}'.format(self.live_server_url, '/register/'))
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys('myuser')
        firstname_input = self.selenium.find_element_by_name("first_name")
        firstname_input.send_keys('foo')
        lastname_input = self.selenium.find_element_by_name("last_name")
        lastname_input.send_keys('bar')
        email_input = self.selenium.find_element_by_name("email")
        email_input.send_keys('example@example123.ch')
        password1_input = self.selenium.find_element_by_name("password1")
        password1_input.send_keys('12345qwert')
        password2_input = self.selenium.find_element_by_name("password2")
        password2_input.send_keys('12345qwert')
