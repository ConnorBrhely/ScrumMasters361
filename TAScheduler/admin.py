from django.contrib import admin
from TAScheduler.models import Course, Section, UserAccount

# Register your models here.
admin.site.register(UserAccount)
admin.site.register(Course)
admin.site.register(Section)
