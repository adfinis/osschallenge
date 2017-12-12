class ProjectPage(object):

    def __init__(self, selenium_driver, live_server_url):
        self.driver = selenium_driver
        self.live_server_url = live_server_url

    def open_page_one_projects(self, page):
        self.driver.get(
            "{}/projects/{}/".format(self.live_server_url, page)
        )
        return self

    def find_active_page(self):
        active_page = self.driver.find_element_by_xpath("//a[@name='active']")
        return active_page
