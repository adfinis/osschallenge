from django.core.management.base import BaseCommand, CommandError
from osschallenge.models import Profile

class Command(BaseCommand):
    help = 'Delete all points for this quarter'

    def handle(self, *args, **options):
        quarter_points = Profile.objects.values('quarter_points')
        quarter_points.update(quarter_points=0)
        self.stdout.write('The quarter points are deleted')


