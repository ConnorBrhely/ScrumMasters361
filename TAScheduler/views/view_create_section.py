from django.shortcuts import render, redirect
from django.views import View
from TAScheduler.models import Section, UserAccount

class CreateSection(View):
    def get(self, request):
        return render(request, "createsection.html", {})

    def post(self, request):
        no_such_section = False
        course = request.POST["course"]
        name = request.POST["name"]
        location = request.POST["location"]

        if course == "" or name == "" or location == "":
            return render(request, "createsection.html", {"message": "One or more blank field detected"})
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
            return render(request, "createsection.html", {
                "message": "Section successfully created",
                "instructors": UserAccount.objects.filter(type="INSTRUCTOR"),
            })
        else:
            return render(request, "createsection.html", {"message": "Section already exists"})