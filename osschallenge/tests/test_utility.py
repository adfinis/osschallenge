from django.test import TestCase
from osschallenge.models import Rank
from osschallenge.templatetags.ranks import get_rank
from osschallenge.views import (
    get_quarter_months,
    get_quarter_start,
    get_next_quarter,)
from freezegun import freeze_time
from datetime import date
from osschallenge.templatetags.shorten import shorten


class UtilityTestCase(TestCase):
    def test_get_rank(self):
        rank1 = Rank.objects.create(name="Jedi Master", required_points=45)
        rank2 = Rank.objects.create(name="Padawan", required_points=15)
        self.assertEqual(get_rank(50), rank1.name)
        self.assertEqual(get_rank(45), rank1.name)
        self.assertEqual(get_rank(10), "-")
        self.assertEqual(get_rank(15), rank2.name)

    def test_get_quarter_months(self):
        self.assertEqual(get_quarter_months("1"), "(January - March)")
        self.assertEqual(get_quarter_months("2"), "(April - June)")
        self.assertEqual(get_quarter_months("3"), "(July - September)")
        self.assertEqual(get_quarter_months("4"), "(October - December)")
        self.assertEqual(get_quarter_months("5"), "-")
        self.assertEqual(get_quarter_months("0"), "-")

    @freeze_time("2017-04-01")
    def test_get_quarter_start(self):
        self.assertEqual(get_quarter_start(), date(2017, 4, 1))

    @freeze_time("2017-01-01")
    def test_get_next_quarter(self):
        self.assertEqual(get_next_quarter(), date(2017, 4, 1))

    def test_shorten(self):
        self.assertEqual(shorten("abc", 2), "ab ...")
        self.assertEqual(shorten("abc", 4), "abc")
        self.assertEqual(shorten("abc", 3), "abc")
