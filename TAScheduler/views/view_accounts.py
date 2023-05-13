from django.shortcuts import render, redirect
from django.views import View
from TAScheduler.models import UserAccount


class Accounts(View):
    def get(self, request):
        users = UserAccount.objects.order_by("type")
        account = UserAccount.objects.get(user_id=request.user.id)
        return render(request, "accounts.html", {"accounts": users, "message": "", "account": account})

    def post(self, request):
        account = UserAccount.objects.get(user_id=request.user.id)
        sort_method = request.POST["sorttype"].strip()
        if sort_method == "name" or sort_method == "namereverse":
            users = UserAccount.objects.order_by("first_name")
            if sort_method == "namereverse":
                users = users.reverse()
        else:
            users = UserAccount.objects.order_by("type")
        return render(request, "accounts.html", {"accounts": users, "account": account})
