from django.test import Client
from django.contrib.auth.models import Group
from osschallenge.models import (
    User,
    Task,
    Comment,
    Rank)
from osschallenge.tests.pages.login import LoginPage
from osschallenge.tests.pages.new_project import NewProjectPage
from osschallenge.tests.pages.new_task import NewTaskPage
from osschallenge.tests.pages.profil import ProfilePage
from osschallenge.tests.pages.task import TaskPage
from osschallenge.tests.pages.ranking import RankingPage
from osschallenge.tests.pages.project import ProjectPage
from osschallenge.tests.pages.rankup import RankUpPage
from osschallenge.tests.selenium_test_options import SeleniumTests
from . import factories


class LoggedInAsContributor(SeleniumTests):

    @classmethod
    def setUpClass(self):
        super(LoggedInAsContributor, self).setUpClass()

    @classmethod
    def setUp(self):
        self.client = Client()
        self.login_page = LoginPage(self.driver, self.live_server_url)
        self.new_project_page = NewProjectPage(
            self.driver, self.live_server_url
        )
        self.new_task_page = NewTaskPage(self.driver, self.live_server_url)
        self.profile_page = ProfilePage(self.driver, self.live_server_url)
        self.task_page = TaskPage(self.driver, self.live_server_url)
        self.ranking_page = RankingPage(self.driver, self.live_server_url)
        self.project_page = ProjectPage(self.driver, self.live_server_url)
        self.rankup_page = RankUpPage(self.driver, self.live_server_url)

        self.user1 = factories.UserFactory(username="Test", first_name="Test")

        self.user1.set_password("12345qwert")
        self.user1.save()

        self.login_page.open()
        self.login_page.login("Test", "12345qwert")

        self.group = Group.objects.create(
            id = 1,
            name = "Contributor"
        )

        self.group.user_set.add(self.user1)

        self.rank1 = Rank.objects.create(
            id=1,
            name="Padawan",
            required_points=0
        )

        self.rank2 = Rank.objects.create(
            id=2,
            name="Youngling",
            required_points=15
        )

        self.rank3 = Rank.objects.create(
            id=7,
            name="Yoda",
            required_points=115
        )

        self.profile1 = factories.ProfileFactory(
            user=self.user1, rank=self.rank3
        )

        self.project1 = factories.ProjectFactory(owner=self.user1)

        self.task1 = Task.objects.create(
            id=1,
            title="Bug Fixing",
            lead_text="Bug Fixing",
            description="Bug Fixing",
            project=self.project1,
            assignee=self.user1,
            task_done=False,
            task_checked=False,
            picture="test.png",
            approved_by=None,
            approval_date="2017-10-18"
        )

        self.task2 = factories.TaskFactory(
            project=self.project1,
            assignee=self.user1,
            task_checked=True,
        )

        self.task3 = factories.TaskFactory(
            project=self.project1,
            assignee=self.user1,
            task_checked=True,
        )

        self.task4 = factories.TaskFactory(
            project=self.project1,
            assignee=self.user1,
            task_checked=True,
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
        super(LoggedInAsContributor, self).tearDownClass()

    def test_write_a_comment(self):
        self.task_page.open(1)
        self.task_page.create_comment("Hallo test")
        comment = Comment.objects.get(comment="Hallo test")
        self.assertEqual(comment.comment, "Hallo test")

    def test_set_profile_inactive(self):
        self.profile_page.open("Test")
        self.profile_page.set_profile_inactive()
        user = User.objects.get(username=self.user1.username)
        self.assertFalse(user.is_active)

    def test_edit_first_name_in_profile(self):
        self.profile_page.open("Test")
        self.profile_page.edit_first_name_in_profile("Foobar")
        user = User.objects.get(username=self.user1.username)
        self.assertEqual(user.first_name, "TestFoobar")

    def test_view_rankup(self):
        self.profile1.rank = self.rank1
        self.profile1.save()
        self.profile_page.open("Test")
        self.profile1.refresh_from_db()
        self.assertEqual(self.profile1.rank_id, 2)

    def test_ranking_page_not_an_integer(self):
        self.ranking_page.open('/ranking/?page=a')
        active_page = self.ranking_page.find_active_page()
        self.assertRaises(ValueError)
        self.assertEquals(int(active_page.text), 1)

    def test_task_page_exists_on_all_tasks(self):
        self.task_page.open_page_one_all_tasks('?page=1')
        active_page = self.task_page.find_active_page()
        self.assertEquals(int(active_page.text), 1)

    def test_task_page_exists_on_my_tasks(self):
        self.task_page.open_page_one_my_tasks('Test', '?page=1')
        active_page = self.task_page.find_active_page()
        self.assertEquals(int(active_page.text), 1)

    def test_project_page_exists(self):
        self.project_page.open_page_one_projects('?page=1')
        active_page = self.project_page.find_active_page()
        self.assertEquals(int(active_page.text), 1)

    def test_redirect_rankup(self):
        self.rankup_page.open()
        element = self.rankup_page.search_element('rankup-message')
        self.assertTrue(element)

    def test_no_redirect_profile(self):
        self.profile_page.open("Test")
        element = self.profile_page.search_element('facebook')
        self.assertTrue(element)
