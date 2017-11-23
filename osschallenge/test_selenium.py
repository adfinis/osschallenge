from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver


class MydriverTests(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super(MydriverTests, cls).setUpClass()
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1200x600')
        cls.driver = webdriver.Chrome(chrome_options=options)
        cls.driver.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super(MydriverTests, cls).tearDownClass()

    def test_login_failed(self):
        self.driver.get('{}{}'.format(self.live_server_url, '/login/'))
        username_input = self.driver.find_element_by_name("username")
        username_input.send_keys('myuser')
        password_input = self.driver.find_element_by_name("password")
        password_input.send_keys('secret')
        self.driver.find_element_by_id("login").click()

    def test_login_and_go_to_mytasks(self):
        self.driver.get('{}{}'.format(self.live_server_url, '/login/'))
        username_input = self.driver.find_element_by_name("username")
        username_input.send_keys('Yelin')
        password_input = self.driver.find_element_by_name("password")
        password_input.send_keys('12345qwert')
        self.driver.find_element_by_id("login").click()
        self.driver.get(
            '{}{}'.format(self.live_server_url, '/my_tasks/Yelin/')
        )

    def test_register(self):
        self.driver.get('{}{}'.format(self.live_server_url, '/register/'))
        username_input = self.driver.find_element_by_name("username")
        username_input.send_keys('myuser')
        firstname_input = self.driver.find_element_by_name("first_name")
        firstname_input.send_keys('foo')
        lastname_input = self.driver.find_element_by_name("last_name")
        lastname_input.send_keys('bar')
        email_input = self.driver.find_element_by_name("email")
        email_input.send_keys('example@example123.ch')
        password1_input = self.driver.find_element_by_name("password1")
        password1_input.send_keys('12345qwert')
        password2_input = self.driver.find_element_by_name("password2")
        password2_input.send_keys('12345qwert')
