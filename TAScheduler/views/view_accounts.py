from django.shortcuts import render, redirect
from django.views import View
from TAScheduler.models import UserAccount


class Accounts(View):
    def get(self, request):
        Users = UserAccount.objects.order_by("type")
        return render(request, "accounts.html", {"accounts": Users, "message": ""})

    def post(self, request):
        sortmethod = request.POST["sorttype"].strip()
        if sortmethod == "email" or sortmethod == "emailreverse":
            Users = UserAccount.objects.order_by("email")
            if sortmethod == "emailreverse":
                Users = Users.reverse()
        elif sortmethod == "name" or sortmethod == "namereverse":
            Users = UserAccount.objects.order_by("first_name")
            if sortmethod == "namereverse":
                Users = Users.reverse()
        else:
            Users = UserAccount.objects.order_by("type")
        return render(request, "accounts.html", {"accounts": Users})




