from django.test import TestCase
from django.test import Client
from django.urls import reverse
from osschallenge.models import (
    Project,
    User,
    Task,
    Profile,
    Role,
    Comment,
    Rank,)


class ViewTestCase(TestCase):
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
        self.user1.set_password("klajsdfkj")
        self.user1.save()

        self.user2 = User.objects.create(
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

        self.user4 = User.objects.create(
            password="klsffajsdfkj",
            last_login="2017-10-18 11:55:45.681893+00",
            is_superuser=False,
            username="example",
            first_name="Test",
            last_name="Test",
            email="example2@example.ch",
            is_staff=False,
            is_active=True,
            date_joined="2017-10-13 08:17:36.901715+00"
        )

        self.user5 = User.objects.create(
            password="klssajsdfkj",
            last_login="2017-10-18 11:55:45.681893+00",
            is_superuser=False,
            username="Fooo",
            first_name="Test",
            last_name="Test",
            email="example@example123.ch",
            is_staff=False,
            is_active=False,
            date_joined="2017-10-13 08:17:36.901715+00"
        )

        self.client.login(
            username="Test",
            password="klajsdfkj"
        )

        self.project = Project.objects.create(
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

        self.project.mentors.add(self.user1)

        self.task1 = Task.objects.create(
            title="Bug Fixing",
            lead_text="Bug Fixing",
            description="Bug Fixing",
            project=self.project,
            assignee=None,
            task_done=False,
            task_checked=False,
            picture="test.png",
            approved_by=None,
            approval_date="2017-10-18 12:34:51.168157+00"
        )

        self.task2 = Task.objects.create(
            title="Edit Code",
            lead_text="Edit Code",
            description="Edit Code",
            project=self.project,
            assignee=self.user1,
            task_done=False,
            task_checked=True,
            picture="test.png",
            approved_by=self.user1,
            approval_date="2017-10-18 12:34:51.168157+00"
        )

        self.task3 = Task.objects.create(
            title="Code",
            lead_text="Code",
            description="Code",
            project=self.project,
            assignee=self.user4,
            task_done=False,
            task_checked=False,
            picture="test.png",
            approved_by=None,
            approval_date="2017-10-18 12:34:51.168157+00"
        )

        self.task4 = Task.objects.create(
            title="Code abc",
            lead_text="Code abc",
            description="Code avc",
            project=self.project,
            assignee=self.user1,
            task_done=True,
            task_checked=False,
            picture="test.png",
            approved_by=None,
            approval_date="2017-10-18 12:34:51.168157+00"
        )

        self.task5 = Task.objects.create(
            title="Do Some",
            lead_text="Do some",
            description="Do some",
            project=self.project,
            assignee=self.user1,
            task_done=True,
            task_checked=True,
            picture="test.png",
            approved_by=self.user1,
            approval_date="2017-10-18 12:34:51.168157+00"
        )

        self.task6 = Task.objects.create(
            title="Make Code",
            lead_text="Make Code",
            description="Make Code",
            project=self.project,
            assignee=self.user1,
            task_done=True,
            task_checked=True,
            picture="test.png",
            approved_by=self.user1,
            approval_date="2017-10-18 12:34:51.168157+00"
        )

        self.role = Role.objects.create(
            id=1,
            name="Contributor"
        )

        self.role = Role.objects.create(
            id=2,
            name="Mentor"
        )

        self.rank3 = Rank.objects.create(
            id=1,
            name="Youngling",
            required_points=0
        )

        self.rank2 = Rank.objects.create(
            id=2,
            name="Padawan",
            required_points=15
        )

        self.rank1 = Rank.objects.create(
            id=3,
            name="Jedi Knight",
            required_points=30
        )

        self.profile1 = Profile.objects.create(
            user=self.user1,
            role=self.role,
            rank=self.rank1,
            links="Test",
            contact="Test",
            key="Test1",
            picture="Test.png"
        )

        self.profile2 = Profile.objects.create(
            user=self.user2,
            role=self.role,
            rank=self.rank1,
            links="Test",
            contact="Test",
            key="Test2",
            picture="Test.png"
        )

        self.profile3 = Profile.objects.create(
            user=self.user3,
            role=self.role,
            rank=self.rank1,
            links="Test",
            contact="Test",
            key=False,
            picture="Test.png"
        )

        self.profile4 = Profile.objects.create(
            user=self.user4,
            role=self.role,
            rank=self.rank1,
            links="Test",
            contact="Test",
            key=123,
            picture="Test.png"
        )

        self.comment1 = Comment.objects.create(
            task=self.task1,
            comment="Test1",
            author=self.user1,
            created_at="2017-10-18 12:34:51.168157+00"
        )

    def test_index_view(self):
        url = reverse('index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'osschallenge/index.html')

    def test_new_project_view(self):
        url = reverse('newproject')
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'osschallenge/newproject.html')

    def test_create_new_project(self):
        url = reverse('newproject')
        response = self.client.post(
            url,
            {
                'title_de': 'test',
                'title_en_us': 'test',
                'lead_text_de': 'test',
                'lead_text_en_us': 'test',
                'description_de': 'test',
                'description_en_us': 'test',
                'licence': 'MIT',
                'github': 'www.example.ch',
                'website': 'www.example.ch',
                'mentors': self.user2.id
            }
        )
        self.assertRedirects(
            response,
            reverse('projectindex'),
            status_code=302
        )

    def test_project_index_view(self):
        url = reverse('projectindex')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'osschallenge/projectindex.html')

    def test_project_view(self):
        url = reverse('project', args=[self.project.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'osschallenge/project.html')

    def test_edit_project_view(self):
        url = reverse('editproject', args=[self.project.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'osschallenge/editproject.html')

    def test_delete_project(self):
        url = reverse('editproject', args=[self.project.pk])
        response = self.client.get(url)
        self.assertEqual(
            response.context['project'].id,
            self.project.pk
        )
        delete_response = self.client.post(url, {'delete-project': 1})
        self.assertRedirects(
            delete_response,
            reverse('projectindex'),
            status_code=302
        )

    def test_redirect_after_edit_project(self):
        url = reverse('editproject', args=[self.project.pk])
        response = self.client.post(
            url,
            {
                'title_de': 'test',
                'title_en_us': 'test',
                'lead_text_de': 'test',
                'lead_text_en_us': 'test',
                'description_de': 'test',
                'description_en_us': 'test',
                'licence': 'MIT',
                'github': 'www.example.ch',
                'website': 'www.example.ch',
                'mentors': self.user1.id
            }
        )
        self.assertRedirects(
            response,
            reverse('project', args=[self.project.pk]),
            status_code=302
        )

    def test_my_task_index_view(self):
        url = reverse('mytask', args=[self.user1.username])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'osschallenge/mytasksindex.html')

    def test_search_match_my_task_index_view(self):
        url = reverse('mytask', args=[self.user1.username])
        response = self.client.get(url, {'search': 'edit'})
        self.assertEqual(
            len(response.context['match_list']),
            1
        )

    def test_search_no_match_my_task_index_view(self):
        url = reverse('mytask', args=[self.user1.username])
        response = self.client.get(url, {'search': 'test'})
        self.assertEqual(
            len(response.context['match_list']),
            0
        )

    def test_task_index_view(self):
        url = reverse('taskindex')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'osschallenge/taskindex.html')

    def test_search_match_task_index_view(self):
        url = reverse('taskindex')
        response = self.client.get(url, {'search': 'edit'})
        self.assertEqual(
            len(response.context['match_list']),
            1
        )

    def test_search_no_match_task_index_view(self):
        url = reverse('taskindex')
        response = self.client.get(url, {'search': 'test'})
        self.assertEqual(
            len(response.context['match_list']),
            0
        )

    def test_task_view(self):
        url = reverse('task', args=[self.task1.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'osschallenge/task.html')

    def test_claim(self):
        # if Claim in request.POST
        url = reverse('task', args=[self.task1.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context['task'].assignee_id,
            None
        )
        claim_response = self.client.post(url, {'Claim': ''})
        self.assertEqual(claim_response.status_code, 200)
        self.assertEqual(
            claim_response.context['task'].assignee_id,
            self.user1.id
        )

    def test_already_claimed(self):
        # if Claim in request.POST and task is already claimed
        url = reverse('task', args=[self.task3.pk])
        response = self.client.post(
            url,
            {'Claim': ''}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context['task'].assignee_id,
            self.user4.id
        )

    def test_release(self):
        # if Release in request.POST
        url = reverse('task', args=[self.task2.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context['task'].assignee_id,
            self.user1.id
        )
        post_response = self.client.post(url, {'Release': ''})
        self.assertEqual(post_response.status_code, 200)
        self.assertEqual(
            post_response.context['task'].assignee_id,
            None
        )

    def test_already_released(self):
        # if Release in request.POST and task is already released
        url = reverse('task', args=[self.task2.pk])
        response = self.client.post(
            url,
            {'Release': ''}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context['task'].assignee_id,
            None
        )

    def test_done(self):
        # if Task done in request.POST
        url = reverse('task', args=[self.task1.pk])
        response = self.client.post(url, {'Task done': ''})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context['task'].assignee_id,
            self.user1.id
        )
        self.assertEqual(
            response.context['task'].task_done,
            True
        )

    def test_already_done(self):
        # if Task done in request.POST and task is already done
        url = reverse('task', args=[self.task4.pk])
        response = self.client.post(
            url,
            {'Task done': ''}
        )
        self.assertEqual(
            response.context['task'].task_done,
            True
        )

    def test_comment(self):
        # if Comment in request.POST
        url = reverse('task', args=[self.task4.pk])
        response = self.client.get(url)
        self.assertEqual(
            len(response.context['comment_list']),
            1
        )
        post_response = self.client.post(
            url,
            {
                'Comment': '',
                'comment': 'Hallo'
            }
        )
        self.assertEqual(post_response.status_code, 200)
        self.assertEqual(
            len(post_response.context['comment_list']),
            2
        )

    def test_comment_is_empty(self):
        # if Comment in request.POST but comment is empty
        url = reverse('task', args=[self.task4.pk])
        response = self.client.get(url)
        self.assertEqual(
            len(response.context['comment_list']),
            1
        )
        post_response = self.client.post(
            url,
            {'Comment': ''}
        )
        self.assertEqual(
            len(post_response.context['comment_list']),
            1
        )

    def test_delete_comment(self):
        # if Delete-comment in request.POST
        url = reverse('task', args=[self.task1.pk])
        response = self.client.get(url)
        self.assertEqual(
            len(response.context['comment_list']),
            1
        )
        delete_response = self.client.post(
            url,
            {'Delete-comment': self.comment1.id}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.comment1.author_id, self.user1.id)
        self.assertEqual(
            len(delete_response.context['comment_list']),
            0
        )

    def test_approve(self):
        # if Approve in request.POST
        url = reverse('task', args=[self.task3.pk])
        response = self.client.post(url, {'Approve': ''})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['task'].task_checked, True)
        self.assertEqual(response.context['task'].approved_by, self.user1)

    def test_already_approved(self):
        # if Task done in request.POST and task is already done
        url = reverse('task', args=[self.task2.pk])
        response = self.client.post(url, {'Approve': ''})
        self.assertEqual(response.context['task'].task_checked, True)
        self.assertEqual(response.context['task'].approved_by, self.user1)

    def test_reopen(self):
        # if Reopen in request.POST
        url = reverse('task', args=[self.task2.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['task'].task_checked, True)
        self.assertEqual(
            response.context['task'].approval_date.strftime(
                "%Y-%m-%d %H:%M:%S.%f+00"
            ),
            "2017-10-18 12:34:51.168157+00"
        )
        post_response = self.client.post(url, {'Reopen': ''})
        self.assertEqual(post_response.status_code, 200)
        self.assertEqual(post_response.context['task'].task_checked, False)
        self.assertEqual(post_response.context['task'].approval_date, None)

    def test_edit_task_view(self):
        url = reverse('edittask', args=[self.task1.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'osschallenge/edittask.html')

    def test_delete_task(self):
        url = reverse('edittask', args=[self.task1.pk])
        response = self.client.get(url)
        self.assertEqual(
            response.context['task'].id,
            self.task1.pk
        )
        delete_response = self.client.post(url, {'Delete-task': 1})
        self.assertRedirects(
            delete_response,
            reverse('taskindex'),
            status_code=302
        )

    def test_edit_task(self):
        url = reverse('edittask', args=[self.task1.pk])
        response = self.client.post(
            url,
            {'title_de': 'example'}
        )
        self.assertRedirects(
            response,
            reverse('task', args=[self.task1.pk]),
            status_code=302
        )

    def test_new_task_view(self):
        url = reverse('newtask', args=[self.project.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'osschallenge/newtask.html')

    def test_create_new_task(self):
        url = reverse('newtask', args=[self.project.pk])
        response = self.client.post(
            url,
            {
                'title_de': 'testbla',
                'title_en_us': 'testbla',
                'lead_text_de': 'testbla',
                'lead_text_en_us': 'testbla',
                'description_de': 'testbla',
                'description_en_us': 'testbla'
            }
        )
        self.assertRedirects(
            response,
            reverse('task', args=[67]),
            status_code=302
        )

    def test_profile_view(self):
        url = reverse('profile', args=[self.user1.username])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'osschallenge/profile.html')

    def test_no_user(self):
        url = reverse('profile', args=['testuser123'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'osschallenge/no_profile_available.html'
        )

    def test_no_profile(self):
        url = reverse('profile', args=[self.user5.username])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'osschallenge/no_profile_available.html'
        )

    def test_profile_does_not_exist_anymore(self):
        url = reverse('profile', args=[self.user2.username])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'osschallenge/profile_does_not_exist.html'
        )

    def test_edit_profile_view(self):
        url = reverse('editprofile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'osschallenge/editprofile.html')

    def test_delete_profile(self):
        url = reverse('editprofile')
        response = self.client.post(
            url,
            {'delete-profile': 1}
        )
        self.assertRedirects(
            response,
            reverse('login'),
            status_code=302
        )

    def test_edit_profile(self):
        url = reverse('editprofile')
        response = self.client.post(
            url,
            {
                'first_name': 'test',
                'contact': 'test',
                'links': 'test'
            }
        )
        self.assertRedirects(
            response,
            reverse('profile', args=[self.user1.username]),
            status_code=302
        )

    def test_task_administration_index_view(self):
        url = reverse('taskadministrationindex')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'osschallenge/task_administration_index.html'
        )

    def test_search_match_administration_index_view(self):
        url = reverse('taskadministrationindex')
        response = self.client.get(url, {'search': 'edit'})
        self.assertEqual(
            len(response.context['match_list']),
            1
        )

    def test_search_no_match_administration_index_view(self):
        url = reverse('taskadministrationindex')
        response = self.client.get(url, {'search': 'test'})
        self.assertEqual(
            len(response.context['match_list']),
            0
        )

    def test_ranking_view(self):
        url = reverse('ranking')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'osschallenge/ranking.html')

    def test_about_view(self):
        url = reverse('about')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'osschallenge/about.html')

    def test_registration_view(self):
        url = reverse('register')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register.html')

    def test_create_user(self):
        url = reverse('register')
        response = self.client.post(
            url,
            {
                'username': 'a',
                'first_name': 'a',
                'last_name': 'a',
                'email': 'a@b.ch',
                'password1': '12345qwert',
                'password2': '12345qwert'
            }
        )
        self.assertRedirects(
            response,
            reverse('registrationsendmail'),
            status_code=302
        )

    def test_registration_done_view(self):
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
            args=["Test14"]
        )
        response_with_invalid_key = self.client.get(url_with_invalid_key)
        self.assertEqual(response_with_invalid_key.status_code, 200)
        self.assertTemplateUsed(
            response_with_invalid_key,
            'osschallenge/registration_failed.html'
        )

    def test_registration_send_mail_view(self):
        url = reverse('registrationsendmail')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'osschallenge/registration_send_mail.html'
        )

    def test_redirect_task_to_rankup_view(self):
        url_tasks = reverse('taskindex')
        response_tasks = self.client.get(url_tasks)
        self.assertEqual(response_tasks.status_code, 200)
        self.assertTemplateUsed(
            response_tasks,
            'osschallenge/taskindex.html'
        )
        self.assertEqual(self.profile1.rank.id, 3)

        self.profile1.rank = self.rank3
        self.profile1.save()

        response_tasks = self.client.get(url_tasks)
        self.assertRedirects(
            response_tasks,
            reverse('rankup'),
            status_code=302
        )

    def test_redirect_mytasks_to_rankup_view(self):
        url_my_tasks = reverse('mytask', args=[self.user1])
        response_my_tasks = self.client.get(url_my_tasks)
        self.assertEqual(response_my_tasks.status_code, 200)
        self.assertTemplateUsed(
            response_my_tasks,
            'osschallenge/mytasksindex.html'
        )
        self.assertEqual(self.profile1.rank.id, 3)

        self.profile1.rank = self.rank3
        self.profile1.save()

        response_my_tasks = self.client.get(url_my_tasks)
        self.assertRedirects(
            response_my_tasks,
            reverse('rankup'),
            status_code=302
        )

    def test_redirect_profile_to_rankup_view(self):
        url_profile = reverse('profile', args=[self.user1])
        response_profile = self.client.get(url_profile)
        self.assertEqual(response_profile.status_code, 200)
        self.assertTemplateUsed(
            response_profile,
            'osschallenge/profile.html'
        )
        self.assertEqual(self.profile1.rank.id, 3)

        self.profile1.rank = self.rank3
        self.profile1.save()

        response_profile = self.client.get(url_profile)
        self.assertRedirects(
            response_profile,
            reverse('rankup'),
            status_code=302
        )

    def test_redirect_rankup_to_home(self):
        url = reverse('rankup')
        response = self.client.get(url)
        self.assertRedirects(response, '/', status_code=301)
