from modeltranslation.translator import register, TranslationOptions
from .models import Project, Task


@register(Project)
class ProjectTranslationOptions(TranslationOptions):
    fields = ('title', 'lead_text', 'description')


@register(Task)
class TaskTranslationOptions(TranslationOptions):
    fields = ('title', 'lead_text', 'description')
