from django import template
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

register = template.Library()


@register.inclusion_tag('pagination.html')
def paging(last_page, current_page, ordered_item_list):
    paginator = Paginator(ordered_item_list, last_page)
    try:
        current_page = int(current_page)
    except ValueError:
        current_page = 1
    except EmptyPage:
        current_page = paginator.num_pages
    previous_page = current_page - 1
    next_page = current_page + 1
    return {
        'current_page': current_page,
        'last_page': last_page,
        'previous_page': previous_page,
        'next_page': next_page,
    }
