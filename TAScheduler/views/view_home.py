from django.shortcuts import render, redirect
from django.views import View
from TAScheduler.models import UserAccount

class Home(View):
    def get(self,request):
        try:
            account = UserAccount.objects.get(user_id=request.user.id)
        except UserAccount.DoesNotExist:
            return redirect("/login")
        return render(request, "home.html", {
            "account": account,
        })

    # def post(self, request):

