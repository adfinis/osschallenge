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
