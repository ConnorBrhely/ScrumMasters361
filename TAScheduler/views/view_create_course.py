from django.shortcuts import render, redirect
from django.views import View
from TAScheduler.models import Course, UserAccount
from django.core.exceptions import PermissionDenied

class CreateCourse(View):
    def get(self, request):
        account = UserAccount.objects.get(user_id=request.user.id)
        if not request.user.is_authenticated:
            return redirect("/login")
        if account.type != "ADMIN":
            raise PermissionDenied
        courses = Course.objects.all()
        instructors = UserAccount.objects.filter(type="INSTRUCTOR")
        return render(request, "createcourse.html", {
            "account": account,
            "courses": courses,
            "instructors": instructors
        })

    def post(self, request):
        no_such_course = False
        name = request.POST["name"].strip()
        number = request.POST["number"].strip()
        term = request.POST["term"].strip()
        instructor = UserAccount.objects.get(pk=int(request.POST["instructor"].strip()))

        message = "Course successfully created"
        status = "success"

        if name == "" or number == "" or term == "" or request.POST["instructor"].strip() == "":
            message = "One or more blank field detected"
            status = "failure"
        try:
            Course.objects.get(number=number, term=term)
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
        else:
            message = "Course already exists"
            status = "failure"
        return render(request, "createcourse.html", {
            "message": message,
            "status": status,
            "account": UserAccount.objects.get(user_id=request.user.id),
            "courses": Course.objects.all(),
            "instructors": UserAccount.objects.filter(type="INSTRUCTOR")
        })