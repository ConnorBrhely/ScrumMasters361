from django.shortcuts import render, redirect
from django.views import View
from TAScheduler.models import UserAccount

class Home(View):
    def get(self,request):
        # If user is not logged in, redirect to login page
        if not request.user.is_authenticated:
            return redirect("/login")

        account = UserAccount.objects.get(user_id=request.user.id)
        return render(request, "home.html", {
            "account": account,
        })
