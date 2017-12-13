from django.test import Client
from osschallenge.models import User, Profile, Role, Project, Task
from osschallenge.tests.pages.login import LoginPage
from osschallenge.tests.pages.register import RegisterPage
from osschallenge.tests.pages.new_project import NewProjectPage
from osschallenge.tests.pages.new_task import NewTaskPage
from osschallenge.tests.selenium_test_options import SeleniumTests


class LoggedInAsMentorTest(SeleniumTests):

    @classmethod
    def setUpClass(self):
        super(LoggedInAsMentorTest, self).setUpClass()

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
        super(LoggedInAsMentorTest, self).tearDownClass()

    def test_create_a_new_project(self):
        self.new_project_page.open()
        new_project = Project(
            title_de="Mein neues Projekt",
            title_en_us="My new project",
            lead_text_de="Einleitung zum Projekt",
            lead_text_en_us="Short introduction to the project",
            description_de="Beschreibung zum Projekt",
            description_en_us="Description for the project",
            licence="GPL",
            github="www.github.com",
            website="www.example.com"
        )
        self.new_project_page.create_new_project(
            new_project.title_de,
            new_project.title_en_us,
            new_project.lead_text_de,
            new_project.lead_text_en_us,
            new_project.description_de,
            new_project.description_en_us,
            new_project.licence,
            new_project.github,
            new_project.website
        )
        project = Project.objects.get(title_de=new_project.title_de)
        self.assertEqual(project.title_de, new_project.title_de)
        self.assertEqual(project.title_en_us, new_project.title_en_us)
        self.assertEqual(project.lead_text_de, new_project.lead_text_de)
        self.assertEqual(
            project.lead_text_en_us, new_project.lead_text_en_us
        )
        self.assertEqual(project.description_de, new_project.description_de)
        self.assertEqual(
            project.description_en_us, new_project.description_en_us
        )
        self.assertEqual(project.licence, new_project.licence)
        self.assertEqual(project.github, new_project.github)
        self.assertEqual(project.website, new_project.website)

    def test_create_a_new_task(self):
        self.new_task_page.open(1)
        new_task = Task(
            title_de="Mein neuer Task",
            title_en_us="My new task",
            lead_text_de="Einleitung zum Task",
            lead_text_en_us="Short introduction to the task",
            description_de="Beschreibung zum Task",
            description_en_us="Description for the task",
        )
        self.new_task_page.create_new_task(
            new_task.title_de,
            new_task.title_en_us,
            new_task.lead_text_de,
            new_task.lead_text_en_us,
            new_task.description_de,
            new_task.description_en_us
        )
        task = Task.objects.get(title_de=new_task.title_de)
        self.assertEqual(task.title_de, new_task.title_de)
        self.assertEqual(task.title_en_us, new_task.title_en_us)
        self.assertEqual(task.lead_text_de, new_task.lead_text_de)
        self.assertEqual(
            task.lead_text_en_us, new_task.lead_text_en_us
        )
        self.assertEqual(task.description_de, new_task.description_de,)
        self.assertEqual(
            task.description_en_us, new_task.description_en_us
        )
