from django.shortcuts import render, redirect
from django.views import View
from TAScheduler.models import UserAccount
from django.core.exceptions import PermissionDenied


class DeleteUser(View):

    def get(self, request):
        autofill = request.GET.get("username")
        if autofill is None:
            return redirect("/accounts")
        try:
            account = UserAccount.objects.get(user_id=request.user.id)
            editaccount = UserAccount.objects.get(user__username=autofill)
            if account == editaccount:
                raise PermissionDenied
            if not request.user.is_authenticated:
                return redirect("/login")
            if account.type != UserAccount.UserType.ADMIN:
                raise PermissionDenied
            return render(request, "deleteuser.html", {"account": account, "editaccount": editaccount})
        except UserAccount.DoesNotExist:
            raise PermissionDenied

    def post(self, request):
        useraccount = request.POST["confirmdelete"]
        editaccount = request.POST["editaccount"]
        editaccount = UserAccount.objects.get(user__email=editaccount)
        message = "User deleted successfully"
        status = "success"
        account = UserAccount.objects.get(user__id=request.user.id)
        if useraccount == "donotdelete":
            message = "Must check box to confirm"
            status = "error"
            return render(request, "deleteuser.html", {
                "message": message,
                "status": status,
                "account": account,
                "editaccount": editaccount
            })
        else:
            deleteaccount = UserAccount.objects.get(user__username=useraccount)
            deleteaccount.user.delete()
            deleteaccount.delete()
            return redirect("/accounts", {"message": message, "status": status, "account": account,
                                                 "accounts": UserAccount.objects.order_by("type")})

