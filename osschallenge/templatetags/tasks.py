from django import template

register = template.Library()


@register.inclusion_tag('tasks.html')
def task_card(task):
    return {
        'task': task
    }
