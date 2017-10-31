from django import template
from osschallenge.models import Rank

register = template.Library()

@register.filter(name='get_rank')
def get_rank(value):
    ranks = Rank.objects.filter(
        required_points__lte=value
        ).order_by('-required_points')[:1]
    return ranks[0]
