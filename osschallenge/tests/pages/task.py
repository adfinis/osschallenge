class TaskPage(object):

    def __init__(self, selenium_driver, live_server_url):
        self.driver = selenium_driver
        self.live_server_url = live_server_url

    def open(self, task_id):
        self.driver.get(
            "{}/tasks/{}/".format(self.live_server_url, task_id)
        )
        return self

    def create_comment(self, comment):
        comment_input = self.driver.find_element_by_id("markdown-comment")
        comment_input.send_keys(comment)
        self.driver.find_element_by_id("comment").click()

    def open_page_one_all_tasks(self, page):
        self.driver.get(
            "{}/tasks/{}".format(self.live_server_url, page)
        )
        return self

    def open_page_one_my_tasks(self, username, page):
        self.driver.get(
            "{}/my_tasks/{}/{}".format(self.live_server_url, username, page,)
        )
        return self

    def find_active_page(self):
        active_page = self.driver.find_element_by_xpath("//a[@name='active']")
        return active_page
