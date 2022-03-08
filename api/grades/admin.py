from django.contrib import admin

from api.grades.models import Grade, Module


admin.site.register(Module)
admin.site.register(Grade)
