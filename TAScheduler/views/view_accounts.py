from django.shortcuts import render, redirect
from django.views import View
from TAScheduler.models import UserAccount


class Accounts(View):
    def get(self, request):
        Users = UserAccount.objects.order_by("type")
        account = UserAccount.objects.get(user_id=request.user.id)
        return render(request, "accounts.html", {"accounts": Users, "message": "", "account": account})

    def post(self, request):
        sortmethod = request.POST["sorttype"].strip()
        if sortmethod == "name" or sortmethod == "namereverse":
            Users = UserAccount.objects.order_by("first_name")
            if sortmethod == "namereverse":
                Users = Users.reverse()
        else:
            Users = UserAccount.objects.order_by("type")
        return render(request, "accounts.html", {"accounts": Users})




