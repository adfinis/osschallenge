from django.contrib import admin

from .models import Project, Task, Account, Role

admin.site.register(Project)
admin.site.register(Task)
admin.site.register(Account)
admin.site.register(Role)
