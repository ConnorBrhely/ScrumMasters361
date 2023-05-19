from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views import View
from TAScheduler.models import UserAccount

class OtherAccount(View):
    def get(self, request):
        # Don't allow non-logged in users to view this page
        if not request.user.is_authenticated:
            redirect("/login")

        account_other = UserAccount.objects.get(pk=request.GET["id"])
        return self.render_simple(request, account_other)

    @staticmethod
    def render_simple(request, account_other: UserAccount, message="", status=""):
        return render(request, "otheraccount.html", {
            "message": message,
            "status": status,
            "account": UserAccount.objects.get(user_id=request.user.id),
            "account_other": account_other,
        })
