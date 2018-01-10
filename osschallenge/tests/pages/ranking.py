class RankingPage(object):

    def __init__(self, selenium_driver, live_server_url):
        self.driver = selenium_driver
        self.live_server_url = live_server_url

    def open(self, page):
        self.driver.get(
            "{}{}".format(self.live_server_url, page)
        )
        return self

    def find_message(self):
        message = self.driver.find_element_by_id('no-users-available')
        return message

    def find_active_page(self):
        active_page = self.driver.find_element_by_css_selector(
            'a[name="active"]'
        )
        return active_page
