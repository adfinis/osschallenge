from selenium.webdriver.support.wait import WebDriverWait


class ProfilePage(object):

    def __init__(self, selenium_driver, live_server_url):
        self.driver = selenium_driver
        self.live_server_url = live_server_url

    def open(self, user_id):
        self.driver.get(
            "{}/profile/{}/".format(self.live_server_url, user_id)
        )
        return self

    def set_profile_inactive(self):
        self.driver.find_element_by_id("edit").click()
        self.driver.find_element_by_id("delete-profile").click()
        self.driver.switch_to.alert.accept()
        WebDriverWait(self.driver, 1).until(
            lambda driver:
            self.driver.current_url == self.live_server_url + '/login/'
        )
        return self

    def edit_first_name_in_profile(self, first_name):
        self.driver.find_element_by_id("edit").click()
        first_name_input = self.driver.find_element_by_name("first_name")
        first_name_input.send_keys(first_name)
        self.driver.find_element_by_id("save").click()

    def search_element(self, id):
        self.driver.find_element_by_id(id)
        return self
