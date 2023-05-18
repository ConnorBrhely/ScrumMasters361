from django.shortcuts import render, redirect
from django.views import View
from TAScheduler.models import UserAccount, Course, Section
from django.core.exceptions import PermissionDenied


class EditCourse(View):
    def get(self, request):
        account = UserAccount.objects.get(user_id=request.user.id)
        if not request.user.is_authenticated:
            return redirect("/login")
        if account.type != UserAccount.UserType.ADMIN:
            raise PermissionDenied
        return self.render_simple1(request)

    def post(self, request):
        name = request.POST["coursename"].strip()
        number = request.POST["coursenumber"].strip()
        term_year = request.POST["courseterm"].strip()
        term_season = request.POST["term_season"]
        instructor = request.POST["courseinstructor"].strip()
        if instructor != "none":
            instructor = UserAccount.objects.get(pk=int(instructor))
        else:
            instructor = None

        if name == "" or number == "" or term_season == "" or term_year == "" or instructor == "":
            return self.render_simple1(request, "One or more blank field detected", "error")

        course_id = request.POST["course_id"]
        course_to_edit = Course.objects.get(pk=course_id)
        course_to_edit.update_name(name)
        course_to_edit.update_number(number)
        course_to_edit.update_term_year=(term_year)
        course_to_edit.update_term_season=(term_season)
        course_to_edit.update_instructor = (instructor)
        return redirect("/courses/", {
            "message": "User edited successfully",
            "status": "success",
            "account": UserAccount.objects.get(user_id=request.user.id),
            "courses": Course.objects.order_by("name")
        })


    def render_simple1(self, request, message="", status="success"):
        course_id = request.GET["id"]
        course_to_edit = Course.objects.get(pk=course_id)
        return render(request, "editcourse.html", {
            "message": message,
            "status": status,
            "account": UserAccount.objects.get(user_id=request.user.id),
            "editcourse": course_to_edit,
            "instructors": UserAccount.objects.filter(type=UserAccount.UserType.INSTRUCTOR)
        })
