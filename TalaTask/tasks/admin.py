from django.contrib import admin
from .models import Employee, Skill, Task

admin.site.register(Employee)
admin.site.register(Task)
admin.site.register(Skill)
