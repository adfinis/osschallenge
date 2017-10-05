from django.test import TestCase
from .models import Profile, Task, User, Role, Rank

class ProfileTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username="Test", password="pbkdf2_sha256$30000$3aYmDdykeXOU$PMOw7spvJ7NTjTI8Pdnu9JJwY2/7AWasDwSvaOPqjK4=", is_staff=False, is_active=True, is_superuser=False)
        role = Role.objects.create(name="Contributor")
        Profile.objects.create(user=user, role=role, points=50, links="www.example.ch", contact="example@example.com", key="lksd231", picture="rofile-pictures/wallpaper-widescreen-landscape-596.jpg")

    def test_get_rank(self):
        test = Profile.objects.get(key="lksd231")
        rank = Rank.objects.create(name="Jedi Master", required_points=45)
        self.assertEqual(test.get_rank(), rank)
