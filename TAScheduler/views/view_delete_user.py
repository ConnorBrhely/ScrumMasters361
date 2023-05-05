from django.shortcuts import render, redirect
from django.views import View
from TAScheduler.models import UserAccount
from django.core.exceptions import PermissionDenied


class DeleteUser(View):

    def get(self, request):
        autofill = request.GET["username"]
        account = UserAccount.objects.get(user_id=request.user.id)
        editaccount = UserAccount.objects.get(user__username=autofill)
        if not request.user.is_authenticated:
            return redirect("/login")
        if account.type != UserAccount.UserType.ADMIN:
            raise PermissionDenied
        return render(request, "deleteuser.html", {"account": account, "editaccount": editaccount})

    def post(self, request):
        confirm = request.POST["confirmdelete"]
        message = "User deleted successfully"
        status = "success"
        account = UserAccount.objects.get(user__id=request.user.id)
        print(confirm)
        if confirm == "donotdelete":
            message = "Must check box to confirm"
            status = "failure"
            return render(request, "deleteuser.html", {
                "message": message,
                "status": status,
                "account": account,
            })
        else:
            deleteaccount = UserAccount.objects.get(user__username=confirm)
            deleteaccount.delete()
            return redirect("/accounts", {"message": message, "status": status, "account": account,
                                                 "accounts": UserAccount.objects.order_by("type")})

