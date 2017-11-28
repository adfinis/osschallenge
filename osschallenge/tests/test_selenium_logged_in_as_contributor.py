from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from django.test import Client
from osschallenge.models import User, Profile, Role, Project, Task, Comment
from osschallenge.tests.pages.login import LoginPage
from osschallenge.tests.pages.register import RegisterPage
from osschallenge.tests.pages.new_project import NewProjectPage
from osschallenge.tests.pages.new_task import NewTaskPage


class MydriverTests(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(self):
        super(MydriverTests, self).setUpClass()
        options = webdriver.ChromeOptions()
        # options.add_argument('headless')
        # options.add_argument('window-size=1200x600')
        self.driver = webdriver.Chrome(chrome_options=options)
        self.driver.implicitly_wait(10)

    @classmethod
    def setUp(self):
        self.client = Client()
        self.login_page = LoginPage(self.driver, self.live_server_url)
        self.register_page = RegisterPage(self.driver, self.live_server_url)
        self.new_project_page = NewProjectPage(
            self.driver, self.live_server_url
        )
        self.new_task_page = NewTaskPage(self.driver, self.live_server_url)

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

        self.login_page.open()
        self.login_page.login("Test", "12345qwert")

        self.role1 = Role.objects.create(
            id=1,
            name="Contributor"
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
    def tearDownClass(self):
        self.driver.quit()
        super(MydriverTests, self).tearDownClass()

    def test_write_a_comment(self):
        self.driver.get("{}{}".format(self.live_server_url, "/tasks/1/"))
        comment_input = self.driver.find_element_by_id("markdown-comment")
        comment_input.send_keys("Hallo test")
        self.driver.find_element_by_id("comment").click()
        comment = Comment.objects.get(comment="Hallo test")
        self.assertEqual(comment.comment, "Hallo test")

    def test_set_profile_inactive(self):
        self.driver.get(
            "{}/profile/{}/".format(self.live_server_url, self.user1.username)
        )
        self.driver.find_element_by_id("edit").click()
        self.driver.find_element_by_id("delete-profile").click()
        self.driver.switch_to.alert.accept()
        WebDriverWait(self.driver, 1).until(
            lambda driver:
            self.driver.current_url == self.live_server_url + '/login/'
        )
        user = User.objects.get(username=self.user1.username)
        self.assertFalse(user.is_active)

    def test_edit_first_name_in_profile(self):
        self.driver.get(
            "{}/profile/{}/".format(self.live_server_url, self.user1.username)
        )
        self.driver.find_element_by_id("edit").click()
        first_name_input = self.driver.find_element_by_name("first_name")
        first_name_input.send_keys("Foobar")
        self.driver.find_element_by_id("save").click()
        user = User.objects.get(username=self.user1.username)
        self.assertEqual(user.first_name, "TestFoobar")
