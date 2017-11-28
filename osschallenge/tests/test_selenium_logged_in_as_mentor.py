from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from django.test import Client
from osschallenge.models import User, Profile, Role, Project, Task
from osschallenge.tests.pages.login import LoginPage
from osschallenge.tests.pages.register import RegisterPage
from osschallenge.tests.pages.new_project import NewProjectPage
from osschallenge.tests.pages.new_task import NewTaskPage


class MydriverTests(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(self):
        super(MydriverTests, self).setUpClass()
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1200x600')
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

        self.login_page.open()
        self.login_page.login("Test", "12345qwert")

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
    def tearDownClass(self):
        self.driver.quit()
        super(MydriverTests, self).tearDownClass()

    def test_create_a_new_project(self):
        self.new_project_page.open()
        self.new_project_page.create_new_project(
            "Mein neues Projekt",
            "My new project",
            "Einleitung zum Projekt",
            "Short introduction to the project",
            "Beschreibung zum Projekt",
            "Description for the project",
            "GPL",
            "www.github.com",
            "www.example.com"
        )
        project = Project.objects.get(title_de="Mein neues Projekt")
        self.assertEqual(project.title_de, "Mein neues Projekt")
        self.assertEqual(project.title_en_us, "My new project")
        self.assertEqual(project.lead_text_de, "Einleitung zum Projekt")
        self.assertEqual(
            project.lead_text_en_us, "Short introduction to the project"
        )
        self.assertEqual(project.description_de, "Beschreibung zum Projekt")
        self.assertEqual(
            project.description_en_us, "Description for the project"
        )
        self.assertEqual(project.licence, "GPL")
        self.assertEqual(project.github, "www.github.com")
        self.assertEqual(project.website, "www.example.com")

    def test_create_a_new_task(self):
        self.new_task_page.open()
        self.new_task_page.create_new_task(
            "Mein neuer Task",
            "My new task",
            "Einleitung zum Task",
            "Short introduction for the task",
            "Beschreibung zum Task",
            "Description for the task"
        )
        task = Task.objects.get(title_de="Mein neuer Task")
        self.assertEqual(task.title_de, "Mein neuer Task")
        self.assertEqual(task.title_en_us, "My new task")
        self.assertEqual(task.lead_text_de, "Einleitung zum Task")
        self.assertEqual(
            task.lead_text_en_us, "Short introduction for the task"
        )
        self.assertEqual(task.description_de, "Beschreibung zum Task")
        self.assertEqual(
            task.description_en_us, "Description for the task"
        )
