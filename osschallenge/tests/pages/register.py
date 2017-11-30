class RegisterPage(object):

    def __init__(self, selenium_driver, live_server_url):
        self.driver = selenium_driver
        self.live_server_url = live_server_url

    def open(self):
        self.driver.get("{}{}".format(self.live_server_url, "/register/"))
        return self

    def register(
            self, user, first_name, last_name, email, password1, password2
    ):
        username_input = self.driver.find_element_by_name("username")
        username_input.send_keys(user)
        firstname_input = self.driver.find_element_by_name("first_name")
        firstname_input.send_keys(first_name)
        lastname_input = self.driver.find_element_by_name("last_name")
        lastname_input.send_keys(last_name)
        email_input = self.driver.find_element_by_name("email")
        email_input.send_keys(email)
        password1_input = self.driver.find_element_by_name("password1")
        password1_input.send_keys(password1)
        password2_input = self.driver.find_element_by_name("password2")
        password2_input.send_keys(password2)
        self.driver.find_element_by_id("register").click()
        return self
