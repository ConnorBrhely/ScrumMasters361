from django.contrib import admin
from TAScheduler.models import Course, Section, User

# Register your models here.
admin.site.register(User)
admin.site.register(Course)
admin.site.register(Section)
