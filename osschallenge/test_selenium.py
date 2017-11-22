from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from django.test import Client
from .models import User, Profile, Role, Project, Task


class MydriverTests(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super(MydriverTests, cls).setUpClass()
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1200x600')
        cls.driver = webdriver.Chrome(chrome_options=options)
        cls.driver.implicitly_wait(10)

    @classmethod
    def setUp(self):
        self.client = Client()

        self.user1 = User.objects.create(
            last_login="2017-10-18 11:55:45.681893+00",
            is_superuser=False,
            username="Test",
            first_name="Test",
            last_name="Test",
            email="example@example.ch",
            is_staff=False,
            is_active=True,
            date_joined="2017-10-13 08:17:36.901715+00"
        )
        self.user1.set_password("12345qwert")
        self.user1.save()

        self.role1 = Role.objects.create(
            id=2,
            name="Mentor"
        )

        self.profile1 = Profile.objects.create(
            user=self.user1,
            role=self.role1,
            links="Test",
            contact="Test",
            key="Test1",
            picture="Test.png"
        )

        self.project1 = Project.objects.create(
            id=1,
            title_de="OpenStreetMap",
            title_en_us="OpenStreetMap",
            lead_text_de="Blablablab",
            lead_text_en_us="Blablablab",
            description_de="Blablablab",
            description_en_us="Blablablab",
            licence="MIT",
            website="www.google.ch",
            github="www.github.com",
            owner=self.user1
        )

        self.task1 = Task.objects.create(
            id=1,
            title="Bug Fixing",
            lead_text="Bug Fixing",
            description="Bug Fixing",
            project=self.project1,
            assignee=None,
            task_done=False,
            task_checked=False,
            picture="test.png",
            approved_by=None,
            approval_date="2017-10-18 12:34:51.168157+00"
        )

        self.client.login(username="Test", password='12345qwert')
        cookie = self.client.cookies['sessionid']
        self.driver.get(self.live_server_url + '/login/')
        self.driver.add_cookie(
            {
                'name': 'sessionid',
                'value': cookie.value,
                'secure': False,
                'path': '/'
            }
        )
        self.driver.refresh()
        self.driver.get(self.live_server_url + '/login/')

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super(MydriverTests, cls).tearDownClass()

    def test_register(self):
        self.driver.get("{}{}".format(self.live_server_url, "/register/"))
        username_input = self.driver.find_element_by_name("username")
        username_input.send_keys("myuser")
        firstname_input = self.driver.find_element_by_name("first_name")
        firstname_input.send_keys("foo")
        lastname_input = self.driver.find_element_by_name("last_name")
        lastname_input.send_keys("bar")
        email_input = self.driver.find_element_by_name("email")
        email_input.send_keys("example@example123.ch")
        password1_input = self.driver.find_element_by_name("password1")
        password1_input.send_keys("12345qwert")
        password2_input = self.driver.find_element_by_name("password2")
        password2_input.send_keys("12345qwert")

    def test_create_a_new_project(self):
        self.driver.get("{}{}".format(self.live_server_url, "/login/"))
        username_input = self.driver.find_element_by_name("username")
        username_input.send_keys("Test")
        password_input = self.driver.find_element_by_name("password")
        password_input.send_keys("12345qwert")
        self.driver.find_element_by_id("login").click()
        self.driver.get(
            "{}{}".format(self.live_server_url, "/projects/")
        )
        self.driver.find_element_by_id("new-project").click()
        title_de_input = self.driver.find_element_by_name("title_de")
        title_de_input.send_keys("Mein neues Projekt")
        title_en_us_input = self.driver.find_element_by_name("title_en_us")
        title_en_us_input.send_keys("My new project")
        lead_text_de_input = self.driver.find_element_by_name("lead_text_de")
        lead_text_de_input.send_keys("Einleitung zum Projekt")
        lead_text_en_us_input = self.driver.find_element_by_name(
            "lead_text_en_us"
        )
        lead_text_en_us_input.send_keys("Short introduction to the project")
        description_de_input = self.driver.find_element_by_name(
            "description_de"
        )
        description_de_input.send_keys("Beschreibung zum Projekt")
        description_en_us_input = self.driver.find_element_by_name(
            "description_en_us"
        )
        description_en_us_input.send_keys("Description to the project")
        licence_input = self.driver.find_element_by_name("licence")
        licence_input.send_keys("GPL")
        github_input = self.driver.find_element_by_name("github")
        github_input.send_keys("www.github.com")
        website_input = self.driver.find_element_by_name("website")
        website_input.send_keys("www.example.com")
        mentor_input = self.driver.find_element_by_xpath(
            "//select/option[@value='242']"
        )
        mentor_input.click()
        self.driver.find_element_by_id("add-project").click()
        self.driver.get("{}{}".format(self.live_server_url, "/projects/"))

    def test_create_a_new_task(self):
        self.driver.get("{}{}".format(self.live_server_url, "/login/"))
        username_input = self.driver.find_element_by_name("username")
        username_input.send_keys("Test")
        password_input = self.driver.find_element_by_name("password")
        password_input.send_keys("12345qwert")
        self.driver.find_element_by_id("login").click()
        self.driver.get(
            "{}{}".format(self.live_server_url, "/projects/1/")
        )
        self.driver.find_element_by_id("new-task").click()
        title_de_input = self.driver.find_element_by_name("title_de")
        title_de_input.send_keys("Mein neues Projekt")
        title_en_us_input = self.driver.find_element_by_name("title_en_us")
        title_en_us_input.send_keys("My new project")
        lead_text_de_input = self.driver.find_element_by_name("lead_text_de")
        lead_text_de_input.send_keys("Einleitung zum Projekt")
        lead_text_en_us_input = self.driver.find_element_by_name(
            "lead_text_en_us"
        )
        lead_text_en_us_input.send_keys("Short introduction to the project")
        description_de_input = self.driver.find_element_by_name(
            "description_de"
        )
        description_de_input.send_keys("Beschreibung zum Projekt")
        description_en_us_input = self.driver.find_element_by_name(
            "description_en_us"
        )
        description_en_us_input.send_keys("Description to the project")
        self.driver.find_element_by_id("add-task").click()

    def test_write_a_comment(self):
        self.driver.get("{}{}".format(self.live_server_url, "/tasks/1/"))
        comment_input = self.driver.find_element_by_id("markdown-comment")
        comment_input.send_keys("Hallo test")
        self.driver.find_element_by_id("comment").click()

    def test_set_profile_inactive(self):
        self.driver.get("{}{}".format(self.live_server_url, "/profile/Test/"))
        self.driver.find_element_by_id("edit").click()
        self.driver.find_element_by_id("delete-profile")

    def test_edit_first_name_in_profile(self):
        self.driver.get("{}{}".format(self.live_server_url, "/profile/Test/"))
        self.driver.find_element_by_id("edit").click()
        first_name_input = self.driver.find_element_by_name("first_name")
        first_name_input.send_keys("Foobar")
        self.driver.find_element_by_id("save").click()
