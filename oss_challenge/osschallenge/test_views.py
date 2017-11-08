from django.test import TestCase
from django.test import Client
from django.urls import reverse
from .models import Project, User, Task, Profile, Role


class ViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        self.user1 = User.objects.create(
            id=1,
            password="klajsdfkj",
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

        self.user2 = User.objects.create(
            id=2,
            password="klajsdfkj",
            last_login="2017-10-18 11:55:45.681893+00",
            is_superuser=False,
            username="Foo",
            first_name="Test",
            last_name="Test",
            email="example@example.ch",
            is_staff=False,
            is_active=False,
            date_joined="2017-10-13 08:17:36.901715+00"
        )

        self.user3 = User.objects.create(
            id=3,
            password="klajsdfkj",
            last_login="2017-10-18 11:55:45.681893+00",
            is_superuser=False,
            username="Bar",
            first_name="Test",
            last_name="Test",
            email="example@example.ch",
            is_staff=False,
            is_active=False,
            date_joined="2017-10-13 08:17:36.901715+00"
        )

        self.client.login(
            username=self.user1.username,
            password=self.user1.password
        )

        self.project = Project.objects.create(
            id=1,
            pk=1,
            title="OpenStreetMap",
            lead_text="Blablablab",
            description="Blablablab",
            licence="MIT",
            website="www.google.ch",
            github="www.github.com",
            owner=self.user1,
            mentors=[1]
        )

        self.task = Task.objects.create(
            id=1,
            pk=1,
            title="Bug Fixing",
            lead_text="Bug Fixing",
            description="Bug Fixing",
            project=self.project,
            assignee=self.user1,
            task_done=False,
            task_checked=False,
            picture="test.png",
            approved_by=self.user1,
            approval_date="2017-10-18 12:34:51.168157+00"
        )

        self.role = Role.objects.create(
            id=1,
            name="Mentor"
        )

        self.profile1 = Profile.objects.create(
            user=self.user1,
            role=self.role,
            links="Test",
            contact="Test",
            key="Test1",
            picture="Test.png"
        )

        self.profile2 = Profile.objects.create(
            user=self.user2,
            role=self.role,
            links="Test",
            contact="Test",
            key="Test2",
            picture="Test.png"
        )

        self.profile3 = Profile.objects.create(
            user=self.user3,
            role=self.role,
            links="Test",
            contact="Test",
            key=False,
            picture="Test.png"
        )

    def test_IndexView(self):
        url = reverse('index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'osschallenge/index.html')

    def test_NewProjectView(self):
        url = reverse('newproject')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'osschallenge/newproject.html')

    def test_ProjectIndexView(self):
        url = reverse('projectindex')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'osschallenge/projectindex.html')

    def test_ProjectView(self):
        url = reverse('project', args=[self.project.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'osschallenge/project.html')

    def test_EditProjectView(self):
        url = reverse('editproject', args=[self.project.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'osschallenge/editproject.html')

    def test_MyTaskIndexView(self):
        url = reverse('task', args=[self.user1.username])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'osschallenge/mytasksindex.html')

    def test_TaskIndexView(self):
        url = reverse('taskindex')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'osschallenge/taskindex.html')

    def test_TaskView(self):
        url = reverse('alltask', args=[self.project.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'osschallenge/task.html')

    def test_EditTaskView(self):
        url = reverse('edittask', args=[self.task.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'osschallenge/edittask.html')

    def test_NewTaskView(self):
        url = reverse('newtask', args=[self.task.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'osschallenge/newtask.html')

    def test_ProfileView(self):
        url = reverse('profile', args=[self.user1.username])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'osschallenge/profile.html')

    def test_ProfileDoesNotExistView(self):
        url = reverse('profile', args=[self.user2.username])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'osschallenge/profile_does_not_exist.html'
        )

    # TODO: Fix this later!!!!!
    # def test_EditProfileView(self):
        # url = reverse('editprofile')
        # response = self.client.get(url)
        # self.assertEqual(response.status_code, 200)
        # self.assertTemplateUsed(response, 'osschallenge/editprofile.html')

    def test_TaskAdministrationIndexView(self):
        url = reverse('taskadministrationindex')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'osschallenge/task_administration_index.html'
        )

    def test_RankingView(self):
        url = reverse('ranking')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'osschallenge/ranking.html')

    def test_AboutView(self):
        url = reverse('about')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'osschallenge/about.html')

    def test_RegistrationView(self):
        url = reverse('register')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register.html')

    def test_RegistrationDoneView(self):
        url_with_inactive_user = reverse(
            'registrationdone',
            args=[self.profile2.key]
        )
        response_with_inactive_user = self.client.get(url_with_inactive_user)
        self.assertEqual(response_with_inactive_user.status_code, 200)
        self.assertTemplateUsed(
            response_with_inactive_user,
            'osschallenge/registration_done.html'
        )

        url_with_active_user = reverse(
            'registrationdone',
            args=[self.profile1.key]
        )
        response_with_active_user = self.client.get(url_with_active_user)
        self.assertEqual(response_with_active_user.status_code, 200)
        self.assertTemplateUsed(
            response_with_active_user,
            'osschallenge/user_is_already_active.html'
        )

        url_with_invalid_key = reverse(
            'registrationdone',
            args=["Test4"]
        )
        response_with_invalid_key = self.client.get(url_with_invalid_key)
        self.assertEqual(response_with_invalid_key.status_code, 200)
        self.assertTemplateUsed(
            response_with_invalid_key,
            'osschallenge/registration_failed.html'
        )

    def test_RegistrationSendMailView(self):
        url = reverse('registrationsendmail')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'osschallenge/registration_send_mail.html'
        )
