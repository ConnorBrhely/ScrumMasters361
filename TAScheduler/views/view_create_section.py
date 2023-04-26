from django.shortcuts import render, redirect
from django.views import View
from TAScheduler.models import Section, UserAccount, Course

class CreateSection(View):
    def get(self, request):
        return render(request, "createsection.html", { "courses": Course.objects.all(), })

    def post(self, request):
        no_such_section = False
        number = request.POST["number"].strip()
        course = request.POST["course"].strip()
        location = request.POST["location"].strip()
        time = request.POST["time"].strip()

        if course == "" or number == "" or location == "":
            return render(request, "createsection.html", {
                "message": "One or more blank field detected",
                "courses": Course.objects.all(),
            })
        try:
            Section.objects.get(number=number)
        except Section.DoesNotExist:
            no_such_section = True
        if no_such_section:
            m = Section.objects.create(
                number=number,
                location=location,
                course=Course.objects.get(pk=int(course)),
                time=time
            )
            m.save()
            return render(request, "createsection.html", {
                "message": "Section successfully created",
                "courses": Course.objects.all(),
            })
        else:
            return render(request, "createsection.html", {
                "message": "Section already exists",
                "courses": Course.objects.all(),
            })