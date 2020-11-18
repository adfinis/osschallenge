class NewTaskPage(object):

    def __init__(self, selenium_driver, live_server_url):
        self.driver = selenium_driver
        self.live_server_url = live_server_url

    def open(self, project_id):
        self.driver.get(
            "{}/projects/{}/new_task".format(self.live_server_url, project_id)
        )
        return self

    def create_new_task(
            self,
            title_de,
            title_en_us,
            lead_text_de,
            lead_text_en_us,
            description_de,
            description_en_us,
            website,
    ):
        title_de_input = self.driver.find_element_by_name("title_de")
        title_de_input.send_keys(title_de)
        title_en_us_input = self.driver.find_element_by_name("title_en_us")
        title_en_us_input.send_keys(title_en_us)
        lead_text_de_input = self.driver.find_element_by_name("lead_text_de")
        lead_text_de_input.send_keys(lead_text_de)
        lead_text_en_us_input = self.driver.find_element_by_name(
            "lead_text_en_us"
        )
        lead_text_en_us_input.send_keys(lead_text_en_us)
        description_de_input = self.driver.find_element_by_name(
            "description_de"
        )
        description_de_input.send_keys(description_de)
        description_en_us_input = self.driver.find_element_by_name(
            "description_en_us"
        )
        description_en_us_input.send_keys(description_en_us)
        website_input = self.driver.find_element_by_name("website")
        website_input.send_keys(website)
        self.driver.find_element_by_id("add-task").click()
