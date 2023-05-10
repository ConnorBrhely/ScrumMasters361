from django.shortcuts import render, redirect
from django.views import View
from TAScheduler.models import Section, UserAccount, Course

class CreateSection(View):
    def get(self, request):
        return render(request, "createsection.html", {
            "courses": Course.objects.all(),
            "account": UserAccount.objects.get(user_id=request.user.id),
        })

    def post(self, request):
        no_such_section = False
        number = request.POST["number"].strip()
        course = request.POST["course"].strip()
        location = request.POST["location"].strip()
        time = request.POST["time"].strip()

        message = "Section successfully created"
        status = "success"

        if course == "" or number == "" or location == "" or time == "":
            message = "One or more blank field detected"
            status = "error"
        try:
            Section.objects.get(number=number, course=course)
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
        else:
            message = "Section already exists"
            status = "error"
        return render(request, "createsection.html", {
            "message": message,
            "status": status,
            "courses": Course.objects.all(),
            "account": UserAccount.objects.get(user_id=request.user.id),
        })