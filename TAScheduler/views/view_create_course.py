from django.shortcuts import render
from django.views import View
from TAScheduler.models import Section, Course, UserAccount

class CreateCourse(View):
    def get(self, request):
        courses = Course.objects.all()
        instructors = UserAccount.objects.filter(type="Instructor")
        return render(request, "createcourse.html", {
            "courses": courses,
            "instructors": instructors
        })

    def post(self, request):
        no_such_section = False
        name = request.POST["name"].strip()
        number = request.POST["number"].strip()
        instructor = UserAccount.objects.get(pk=int(request.POST["instructor"].strip()))

        if name == "" or number == "" or request.POST["instructor"].strip() == "":
            return render(request, "createcourse.html", {"message": "One or more blank field detected"})
        try:
            m = Course.objects.get(number=number)
        except Section.DoesNotExist:
            no_such_section = True
        if no_such_section:
            m = Section()
            m.course = course
            m.name = name
            m.location = location
            m.save()
            return render(request, "createsection.html", {"message": "Section successfully created"})
        else:
            return render(request, "createsection.html", {"message": "Section already exists"})