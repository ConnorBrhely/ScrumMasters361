from django.shortcuts import render, redirect
from django.views import View
from TAScheduler.models import UserAccount

class Courses(View):

    def get(self, request):
        # If the user is not logged in, redirect them to the login page
        if not request.user.is_authenticated:
            return redirect("/login")
        account = UserAccount.objects.get(user_id=request.user.id)

        # Sort by name by default
        courses = account.get_courses().order_by("name")

        return render(request, "courses.html", {"courses": courses, "account": account})

    def post(self, request):
        account = UserAccount.objects.get(user_id=request.user.id)
        courses = account.get_courses()
        course_to_delete = request.POST.get("delete")

        # If course_to_delete is not None, then the user clicked the delete button
        if course_to_delete is not None:
            courses.get(id=course_to_delete).delete()
            return redirect("/courses")

        # If course_to_delete is None, then the user just wants to view the courses
        sort_method = request.POST["sorttype"].strip()
        if sort_method == "coursenumber":
            courses = courses.order_by("number")
        elif sort_method == "coursenumberreverse":
            courses = courses.order_by("number").reverse()
        elif sort_method == "name":
            courses = courses.order_by("name")
        else:
            # Unknown sort method, default to sorting by name
            courses = courses.order_by("name")
            return render(request, "courses.html", {
                "courses": courses,
                "account": account,
                "sort_method": sort_method,
                "message": "Invalid sort method",
                "status": "error"
            })
        return render(request, "courses.html", {"courses": courses, "account": account, "sort_method": sort_method})






