import factory
from .. import models


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.User

    last_login = "2017-11-24 09:54:02.784094+00"
    is_superuser = False
    username = factory.Faker('user_name')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('ascii_safe_email')
    is_staff = False
    is_active = True
    date_joined = "2017-11-24 09:54:02.784094+00"


class RoleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Role

    name = factory.Faker('word')


class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Profile

    user = factory.SubFactory(UserFactory)
    role = "Replace"
    key = factory.Faker(
        'password', length=10, special_chars=False,
        digits=True, upper_case=True, lower_case=True)
    links = factory.Faker('domain_name')
    contact = factory.Faker('ascii_safe_email')
    picture = "example.jpg"


class ProjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Project

    title = factory.Sequence(lambda n: "Project %s" % n)
    lead_text = factory.Faker('text', max_nb_chars=100)
    description = factory.Faker('sentences', nb=10)
    licence = "GPL-3.0"
    website = factory.Faker('domain_name')
    github = factory.Faker('domain_name')
    owner = factory.SubFactory(UserFactory)
    active = True

    # ProjectFactory.create(mentors=(mentor1, mentor2))
    @factory.post_generation
    def mentors(self, create, extracted,  **kwargs):
        if not create:
            return

        if extracted:
            for mentor in extracted:
                self.mentors.add(mentor)


class TaskFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Task

    title = factory.Sequence(lambda n: "Task %s" % n)
    lead_text = factory.Faker('text', max_nb_chars=100)
    description = factory.Faker('sentences', nb=10)
    project = factory.SubFactory(ProjectFactory)
    assignee = factory.SubFactory(UserFactory)
    task_done = False
    task_checked = False
    picture = "oss-challenge.jpg"
    approved_by = factory.SubFactory(UserFactory)
    approval_date = "2017-10-18 12:34:51.168157+00"


class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Comment

    task = factory.SubFactory(TaskFactory)
    comment = "Test1"
    author = factory.SubFactory(UserFactory)
    created_at = "2017-11-24 09:54:02.784094+00"
