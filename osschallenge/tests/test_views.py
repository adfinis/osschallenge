from django.test import TestCase
from django.test import Client
from django.urls import reverse
from . import factories
from osschallenge.models import Rank
from django.contrib.auth.models import Group


class ViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        self.user1 = factories.UserFactory(username="Test")
        self.user2 = factories.UserFactory(username="Foo", is_active=False)
        self.user3 = factories.UserFactory(username="Bar", is_active=False)
        self.user4 = factories.UserFactory(username="example")
        self.user5 = factories.UserFactory(username="Fooo", is_active=False)

        self.user1.set_password("klajsdfkj")
        self.user1.save()

        self.client.login(
            username="Test",
            password="klajsdfkj"
        )

        self.project = factories.ProjectFactory(owner=self.user1)

        self.group1 = Group.objects.create(
            id = 1,
            name = "Contributor"
        )

        self.group2 = Group.objects.create(
            id = 2,
            name = "Mentor"
        )

        self.group2.user_set.add(self.user1)
        self.group2.user_set.add(self.user2)
        self.group1.user_set.add(self.user3)
        self.group1.user_set.add(self.user4)

        self.project.mentors.add(self.user1)

        self.task1 = factories.TaskFactory(project=self.project, assignee=None)

        self.task2 = factories.TaskFactory(
            title="Edit Code",
            project=self.project,
            assignee=self.user4,
            task_checked=True,
            approved_by=self.user1
        )

        self.task3 = factories.TaskFactory(
            title="Code", project=self.project, assignee=self.user4
        )

        self.task4 = factories.TaskFactory(
            title="Code abc",
            project=self.project,
            assignee=self.user1,
            task_done=True
        )

        self.task5 = factories.TaskFactory(
            project=self.project, assignee=self.user1, task_checked=True
        )

        self.task6 = factories.TaskFactory(
            title="Make Code",
            project=self.project,
            assignee=self.user1,
            task_checked=True
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

        self.profile1 = factories.ProfileFactory(
            user=self.user1, rank=self.rank1
        )

        self.profile2 = factories.ProfileFactory(
            user=self.user2, rank=self.rank1
        )

        self.profile3 = factories.ProfileFactory(
            user=self.user3, rank=self.rank1, key=False
        )

        self.profile4 = factories.ProfileFactory(
            user=self.user4, rank=self.rank1, key=123

        )

        self.comment = factories.CommentFactory(
            author=self.user1, task=self.task1
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
                'mentors': self.user1.id
            }
        )
        self.assertRedirects(
            response,
            reverse('projectindex'),
            status_code=302
        )

    def test_project_index_view(self):
        self.group2.user_set.remove(self.user1)
        url = reverse('projectindex')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'osschallenge/projectindex.html')

    def test_project_index_view_mentor(self):
        url = reverse('projectindex')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'osschallenge/projectindex.html')

    def test_project_index_view_contributor(self):
        self.group2.user_set.remove(self.user1)
        self.group1.user_set.add(self.user1)
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
        self.assertTemplateUsed(response, 'osschallenge/taskindex.html')

    def test_search_match_my_task_index_view(self):
        url = reverse('mytask', args=[self.user4.username])
        response = self.client.get(url, {'search': 'code'})
        self.assertEqual(
            len(response.context['tasks']),
            2
        )

    def test_search_no_match_my_task_index_view(self):
        url = reverse('mytask', args=[self.user1.username])
        response = self.client.get(url, {'search': 'test'})
        self.assertEqual(
            len(response.context['tasks']),
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
            len(response.context['tasks']),
            1
        )

    def test_search_no_match_task_index_view(self):
        url = reverse('taskindex')
        response = self.client.get(url, {'search': 'test'})
        self.assertEqual(
            len(response.context['tasks']),
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
        user = factories.UserFactory()
        task = factories.TaskFactory(project=self.project, assignee=user)
        url = reverse('task', args=[task.pk])
        response = self.client.post(
            url,
            {'Claim': ''}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context['task'].assignee_id, user.id
        )

    def test_release(self):
        # if Release in request.POST
        url = reverse('task', args=[self.task2.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context['task'].assignee_id,
            self.user4.id
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
        task = factories.TaskFactory(task_done=True)
        url = reverse('task', args=[task.pk])
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
            {'Delete-comment': self.comment.id}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.comment.author_id, self.user1.id)
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
            response.context['task'].approval_date.strftime("%Y-%m-%d"),
            "2017-10-18"
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
        self.assertEqual(response.status_code, 200)

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
        self.assertEqual(response.status_code, 200)

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
        account = factories.UserFactory(is_active = False)
        url = reverse('profile', args=[account.username])
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

    def test_task_admin_view(self):
        url = reverse('admin')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'osschallenge/taskindex.html'
        )

    def test_search_match_admin_view(self):
        url = reverse('admin')
        response = self.client.get(url, {'search': 'code abc'})
        self.assertEqual(
            len(response.context['tasks']),
            1
        )

    def test_search_no_match_admin_view(self):
        url = reverse('admin')
        response = self.client.get(url, {'search': 'test'})
        self.assertEqual(
            len(response.context['tasks']),
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
        url_my_tasks = reverse('mytask', args=[self.user1.username])
        response_my_tasks = self.client.get(url_my_tasks)
        self.assertEqual(response_my_tasks.status_code, 200)
        self.assertTemplateUsed(
            response_my_tasks,
            'osschallenge/taskindex.html'
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
        self.assertEqual(self.profile1.rank_id, 3)

        self.profile1.rank = self.rank3
        self.profile1.save()

        response_profile = self.client.get(url_profile)
        self.assertRedirects(
            response_profile,
            reverse('rankup'),
            status_code=302
        )

    def test_error_404_page(self):
        response = self.client.get('thereisnopagehere')
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, 'osschallenge/404.html')
