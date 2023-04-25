from django.shortcuts import render
from django.views import View
from TAScheduler.models import Section, UserAccount

class CreateCourse(View):
    def get(self, request):
        instructors = UserAccount.objects.filter(type="Instructor")
        # entry = UserAccount.objects.get(pk=2)
        # print(entry.type)
        # print("Entry: " + entry.first_name + " " + entry.last_name)
        # for i in instructors:
        #     print(i.first_name + " " + i.last_name)
        return render(request, "createcourse.html", {
            "instructors": instructors
        })

    def post(self, request):
        no_such_section = False
        course = request.POST["course"].strip()
        name = request.POST["name"].strip()
        location = request.POST["location"].strip()

        if course == "" or name == "" or location == "":
            return render(request, "createcourse.html", {"message": "One or more blank field detected"})
        try:
            m = Section.objects.get(name=name)
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