from django.shortcuts import render, redirect
from django.views import View
from TAScheduler.models import Section, UserAccount, Course

class CreateSection(View):
    def get(self, request):
        return self.render_simple(request)

    def post(self, request):
        number = request.POST["number"].strip()
        course = request.POST["course"].strip()
        location = request.POST["location"].strip()
        time = request.POST["time"].strip()

        if course == "" or number == "" or location == "" or time == "":
            return self.render_simple(request, "One or more blank field detected", "error")
        try:
            # Check if section already exists, should not reach return if section does not exist
            Section.objects.get(number=number, course=course)
            return self.render_simple(request, "Section already exists", "error")
        except Section.DoesNotExist:
            new_section = Section.objects.create(
                number=number,
                location=location,
                course=Course.objects.get(pk=int(course)),
                time=time
            )
            new_section.save()

        return self.render_simple(request, "Section successfully created")

    @staticmethod
    def render_simple(request, message="", status="success"):
        return render(request, "createsection.html", {
            "message": message,
            "status": status,
            "courses": Course.objects.all(),
            "account": UserAccount.objects.get(user_id=request.user.id),
        })