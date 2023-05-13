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
        """User account is either email or 'donotdelete' if box isnt checked"""
        """Edit acount is the name of the account regardless in order to autofill form if submitted without check off"""
        account_to_edit = request.POST["editaccount"]
        account_to_edit = UserAccount.objects.get(user__email=account_to_edit)
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
                "editaccount": account_to_edit
            })
        else:
            account_to_delete = UserAccount.objects.get(user__username=useraccount)
            account_to_delete.user.delete()
            account_to_delete.delete()
            return redirect("/accounts", {"message": message, "status": status, "account": account,
                                                 "accounts": UserAccount.objects.order_by("type")})

