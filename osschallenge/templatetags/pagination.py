from django import template

register = template.Library()


@register.inclusion_tag('pagination.html')
def paging(last_page, current_page, ordered_item_list):
    try:
        current_page = int(current_page)
    except ValueError:
        current_page = 1
    previous_page = current_page - 1
    next_page = current_page + 1
    return {
        'current_page': current_page,
        'last_page': last_page,
        'previous_page': previous_page,
        'next_page': next_page,
    }
