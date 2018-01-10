class RankUpPage(object):

    def __init__(self, selenium_driver, live_server_url):
        self.driver = selenium_driver
        self.live_server_url = live_server_url

    def open(self):
        self.driver.get("{}/rankup/".format(self.live_server_url))
        return self

    def search_element(self, class_name):
        self.driver.find_element_by_class_name(class_name)
        return self
