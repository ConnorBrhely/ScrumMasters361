from django.shortcuts import render, redirect
from django.views import View
from TAScheduler.models import UserAccount, Course, Section
from django.core.exceptions import PermissionDenied
from ..common import validate

class EditCourse(View):
    def get(self, request):
        account = UserAccount.objects.get(user_id=request.user.id)

        # If user is not properly authenticated, redirect to login page
        if not request.user.is_authenticated:
            return redirect("/login")
        if account.type != UserAccount.UserType.ADMIN:
            raise PermissionDenied

        return self.render_simple(request)

    def post(self, request):
        name = request.POST["coursename"].strip()
        number = request.POST["coursenumber"].strip()
        term_year = request.POST["courseterm"].strip()
        term_season = request.POST["term_season"]
        instructor = request.POST["courseinstructor"].strip()

        # Allow no instructor to be specified
        if instructor == "none":
            instructor = None
        else:
            instructor = UserAccount.objects.get(pk=int(instructor))

        # Check for blank fields
        if name == "" or number == "" or term_season == "" or term_year == "":
            return self.render_simple(request, "One or more blank field detected", "error")

        # Validate input
        if not validate.course_number(number):
            return self.render_simple(request, "Invalid course number", "error")
        if not validate.year(term_year):
            return self.render_simple(request, "Invalid term year", "error")
        if instructor is not None and instructor.type != UserAccount.UserType.INSTRUCTOR:
            return self.render_simple(request, "Specified user is not an instructor", "error")

        course_id = request.POST["course_id"]
        course_to_edit = Course.objects.get(pk=course_id)

        # Update course
        course_to_edit.update_name(name)
        course_to_edit.update_number(number)
        course_to_edit.update_term_year(term_year)
        course_to_edit.update_term_season(term_season)
        course_to_edit.update_instructor(instructor)

        return self.render_simple(request, "Course successfully edited")

    def render_simple(self, request, message="", status="success"):
        course_id = request.GET["id"]
        course_to_edit = Course.objects.get(pk=course_id)

        return render(request, "editcourse.html", {
            "message": message,
            "status": status,
            "account": UserAccount.objects.get(user_id=request.user.id),
            "editcourse": course_to_edit,
            "instructor": course_to_edit.instructor,
            "instructors": UserAccount.objects.filter(type=UserAccount.UserType.INSTRUCTOR)
        })
