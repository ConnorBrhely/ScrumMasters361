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
        return self.render_simple(request)

    def post(self, request):
        no_such_course = False
        name = request.POST["name"].strip()
        number = request.POST["number"].strip()
        term_season = request.POST["term_season"].strip()
        term_year = request.POST["term_year"].strip()
        instructor = UserAccount.objects.get(pk=int(request.POST["instructor"].strip()))

        if name == "" or number == "" or term_season == "" or term_year == "" or request.POST["instructor"].strip() == "":
            return self.render_simple(request, "One or more blank field detected", "error")
        try:
            Course.objects.get(number=number, term_season=term_season, term_year=term_year)
        except Course.DoesNotExist:
            no_such_course = True
        if no_such_course:
            m = Course.objects.create(
                name=name,
                number=number,
                term_season=term_season,
                term_year=term_year,
                instructor=instructor
            )
            m.save()
        else:
            return self.render_simple(request, "Course already exists", "error")

        return self.render_simple(request, "Course successfully created")

    @staticmethod
    def render_simple(request, message="", status="success"):
        user = request.user
        return render(request, "createcourse.html", {
            "message": message,
            "status": status,
            "account": UserAccount.objects.get(user_id=user.id),
            "terms": Course.TERM_SEASON_CHOICES,
            "courses": Course.objects.all(),
            "instructors": UserAccount.objects.filter(type="INSTRUCTOR")
        })