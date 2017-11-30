class NewProjectPage(object):

    def __init__(self, selenium_driver, live_server_url):
        self.driver = selenium_driver
        self.live_server_url = live_server_url

    def open(self):
        self.driver.get("{}{}".format(self.live_server_url, "/projects/"))
        self.driver.find_element_by_id("new-project").click()
        return self

    def create_new_project(
            self,
            title_de,
            title_en_us,
            lead_text_de,
            lead_text_en_us,
            description_de,
            description_en_us,
            licence,
            github,
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
        licence_input = self.driver.find_element_by_name("licence")
        licence_input.send_keys(licence)
        github_input = self.driver.find_element_by_name("github")
        github_input.send_keys(github)
        website_input = self.driver.find_element_by_name("website")
        website_input.send_keys(website)
        mentor_input = self.driver.find_element_by_xpath(
            "//select[@id='id_mentors']/option[text()='Test']"
        )
        mentor_input.click()
        self.driver.find_element_by_id("add-project").click()
        self.driver.get("{}{}".format(self.live_server_url, "/projects/"))
        return self
