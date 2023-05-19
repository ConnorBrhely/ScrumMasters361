from django.shortcuts import render, redirect
from django.views import View
from TAScheduler.models import Course, UserAccount
from django.core.exceptions import PermissionDenied

class CreateCourse(View):
    def get(self, request):
        # Check if user is logged in
        account = UserAccount.objects.get(user_id=request.user.id)
        if not request.user.is_authenticated:
            return redirect("/login")

        # Only admins can create courses
        if account.type != UserAccount.UserType.ADMIN:
            raise PermissionDenied

        return self.render_simple(request)

    def post(self, request):
        name = request.POST["name"].strip()
        number = request.POST["number"].strip()
        instructor = request.POST["instructor"].strip()

        # Extract term season and year from term_season
        season_string = request.POST["term_season"].strip().split()
        term_season = season_string[0]
        term_year = season_string[1]

        # If instructor is "none", no instructor is assigned
        if instructor == "none":
            instructor = None
        else:
            instructor = UserAccount.objects.get(pk=int(instructor))
        if name == "" or number == "" or term_season == "" or term_year == "" or request.POST["instructor"].strip() == "":
            return self.render_simple(request, "One or more blank field detected", "error")
        try:
            # Attempt to get a course with the same number and term, will only reach the return statement if it exists
            Course.objects.get(number=number, term_season=term_season, term_year=term_year)
            return self.render_simple(request, "Course already exists", "error")
        except Course.DoesNotExist:
            new_course = Course.objects.create(
                name=name,
                number=number,
                term_season=term_season,
                term_year=term_year,
                instructor=instructor
            )
            new_course.save()

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