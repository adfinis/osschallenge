from django.test import TestCase
from .models import Rank
from templatetags.ranks import get_rank
from .views import shorten, get_quarter_months


class UtilityTestCase(TestCase):
    def test_get_rank(self):
        rank1 = Rank.objects.create(name="Jedi Master", required_points=45)
        rank2 = Rank.objects.create(name="Padawan", required_points=15)
        self.assertEqual(get_rank(50), rank1.name)
        self.assertEqual(get_rank(45), rank1.name)
        self.assertEqual(get_rank(10), "-")
        self.assertEqual(get_rank(15), rank2.name)

    def test_shorten(self):
        self.assertEqual(shorten("abc", 2), "ab ...")
        self.assertEqual(shorten("abc", 4), "abc")
        self.assertEqual(shorten("abc", 3), "abc")

    def test_get_quarter_months(self):
        self.assertEqual(get_quarter_months("1"), "(January - March)")
        self.assertEqual(get_quarter_months("2"), "(April - June)")
        self.assertEqual(get_quarter_months("3"), "(July - September)")
        self.assertEqual(get_quarter_months("4"), "(October - December)")
        self.assertEqual(get_quarter_months("5"), "-")
        self.assertEqual(get_quarter_months("0"), "-")
