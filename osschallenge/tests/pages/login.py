class LoginPage(object):

    def __init__(self, selenium_driver, live_server_url):
        self.driver = selenium_driver
        self.live_server_url = live_server_url

    def open(self):
        self.driver.get("{}{}".format(self.live_server_url, "/login/"))
        return self

    def login(self, user, password):
        username_input = self.driver.find_element_by_name("username")
        username_input.send_keys(user)
        password_input = self.driver.find_element_by_name("password")
        password_input.send_keys(password)
        self.driver.find_element_by_id("login").click()
        return self

    def logout(self):
        self.driver.find_element_by_id("logout").click()
        return self
