from django.shortcuts import render, redirect
from django.views import View
from TAScheduler.models import UserAccount, Course, model_section
from django.core.exceptions import PermissionDenied


class EditCourse(View):

    def get(self, request):
        course = request.GET["name"]
        account = UserAccount.objects.get(user_id=request.user.id)
        if not request.user.is_authenticated:
            return redirect("/login")
        if account.type != UserAccount.UserType.ADMIN:
            raise PermissionDenied
        return render(request, "editcourse.html", {"message": "hello world", "account": account, "course": course})



    def post(self, request):
        pass
