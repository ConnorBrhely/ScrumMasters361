from django.shortcuts import render, redirect
from django.views import View
from TAScheduler.models import UserAccount, Course

class Courses(View):

    def get(self, request):
        account = UserAccount.objects.get(user_id=request.user.id)
        courses = Course.objects.order_by("name")
        return render(request, "courses.html", {"courses": courses, "account": account})

    def post(self, request):
        account = UserAccount.objects.get(user_id=request.user.id)
        course_to_delete = request.POST.get("delete")
        if course_to_delete is not None:
            Course.objects.get(id=course_to_delete).delete()
            return redirect("/courses")
        sort_method = request.POST["sorttype"].strip()
        if sort_method == "coursenumber" or sort_method == "coursenumberreverse":
            courses = Course.objects.order_by("number")
            if sort_method == "coursenumberreverse":
                courses = courses.reverse()
        else:
            courses = Course.objects.order_by("name")
        return render(request, "courses.html", {"courses": courses, "account": account, "sort_method": sort_method})






