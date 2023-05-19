from django.shortcuts import render, redirect
from django.views import View
from TAScheduler.models import UserAccount

class Courses(View):

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect("/login")
        account = UserAccount.objects.get(user_id=request.user.id)
        courses = account.get_courses().order_by("name")
        return render(request, "courses.html", {"courses": courses, "account": account})

    def post(self, request):
        account = UserAccount.objects.get(user_id=request.user.id)
        courses = account.get_courses()
        print(len(courses))
        course_to_delete = request.POST.get("delete")
        if course_to_delete is not None:
            courses.get(id=course_to_delete).delete()
            return redirect("/courses")
        sort_method = request.POST["sorttype"].strip()
        if sort_method == "coursenumber" or sort_method == "coursenumberreverse":
            courses = courses.order_by("number")
            print("a")
            print(len(courses))
            if sort_method == "coursenumberreverse":
                courses = courses.reverse()
                print("b")
                print(len(courses))
        else:
            courses = courses.order_by("name")
            print("c")
            print(len(courses))
        return render(request, "courses.html", {"courses": courses, "account": account, "sort_method": sort_method})






