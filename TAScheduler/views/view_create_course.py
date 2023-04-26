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
        no_such_course = False
        name = request.POST["name"].strip()
        number = request.POST["number"].strip()
        term = request.POST["term"].strip()
        instructor = UserAccount.objects.get(pk=int(request.POST["instructor"].strip()))

        if name == "" or number == "" or term == "" or request.POST["instructor"].strip() == "":
            return render(request, "createcourse.html", {"message": "One or more blank field detected"})
        try:
            Course.objects.get(number=number)
        except Course.DoesNotExist:
            no_such_course = True
        if no_such_course:
            m = Course.objects.create(
                name=name,
                number=number,
                term=term,
                instructor=instructor
            )
            m.save()
            return render(request, "createcourse.html", {
                "message": "Section successfully created",
                "courses": Course.objects.all(),
                "instructors": UserAccount.objects.filter(type="Instructor")
            })
        else:
            return render(request, "createcourse.html", {
                "message": "Section already exists",
                "courses": Course.objects.all(),
                "instructors": UserAccount.objects.filter(type="Instructor")
            })