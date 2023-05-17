from django.shortcuts import render, redirect
from django.views import View
from TAScheduler.models import UserAccount, Course, model_section
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
        course = request.GET["course"]
        name=request.POST["name"].strip()
        number=request.POST["number"].strip()
        s = request.POST["term_season"].strip()
        s = s.split()
        term_season = s[0]
        term_year = s[1]
        instructor = UserAccount.objects.get(pk=int(request.POST["instructor"].strip()))
        if name == "" or number == "" or term_season == "" or term_year == "" or request.POST["instructor"].strip() == "":
            return self.render_simple1(request, "One or more blank field detected", "error")
        try:
            Course.objects.get(name=course.name, number=course.number, term_season=course.term_season, term_year=course.term_year)
        except Course.DoesNotExist:
            no_such_course = True
        if not no_such_course:


    def render_simple1(request, message="", status="success"):
        course_id = request.GET["id"]
        course_to_edit = Course.objects.get(pk=course_id)
        return render(request, "editcourse.html", {
            "message": message,
            "status": status,
            "account": UserAccount.objects.get(user_id=request.user.id),
            "editcourse": course_to_edit,
            "tas_in_section": course_to_edit.get_tas(),
            "tas": UserAccount.objects.filter(type=UserAccount.UserType.TA),

        })
