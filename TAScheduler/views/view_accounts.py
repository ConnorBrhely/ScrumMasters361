from django.shortcuts import render, redirect
from django.views import View
from TAScheduler.models import UserAccount


class Accounts(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect("/login")
        users = UserAccount.objects.order_by("type")
        account = UserAccount.objects.get(user_id=request.user.id)
        users = list(users)
        sort_method = "type"
        return render(request, "accounts.html", {"accounts": users, "message": "", "account": account, "sorttype": sort_method})

    def post(self, request):
        account = UserAccount.objects.get(user_id=request.user.id)
        sort_method = request.POST["sorttype"].strip()

        if sort_method == "name":
            users = UserAccount.objects.order_by("first_name")
        elif sort_method == "namereverse":
            users = UserAccount.objects.order_by("first_name").reverse()
        elif sort_method == "type":
            users = UserAccount.objects.order_by("type")
        else:
            # Default to sorting by type
            users = UserAccount.objects.order_by("type")
            return render(request, "accounts.html", {
                "accounts": users,
                "account": account,
                "sorttype": sort_method,
                "message": "Invalid sort method",
                "status": "error"
            })

        users = list(users)
        return render(request, "accounts.html", {"accounts": users, "account": account, "sorttype": sort_method})
