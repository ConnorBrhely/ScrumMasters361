from django.shortcuts import render, redirect
from django.views import View
from TAScheduler.models import UserAccount
from django.core.exceptions import PermissionDenied


class DeleteUser(View):

    def get(self, request):
        autofill = request.GET.get("username")
        if autofill is None:
            # If no username is provided, redirect to accounts page
            return redirect("/accounts")

        try:
            account = UserAccount.objects.get(user_id=request.user.id)
            edit_account = UserAccount.objects.get(user__username=autofill)

            # If user is not properly authenticated, redirect to login page
            if not request.user.is_authenticated:
                return redirect("/login")
            if account.type != UserAccount.UserType.ADMIN:
                raise PermissionDenied

            # Don't let user delete themselves
            if account == edit_account:
                raise PermissionDenied

            return render(request, "deleteuser.html", {"account": account, "editaccount": edit_account})
        except UserAccount.DoesNotExist:
            raise ValueError("User does not exist")

    def post(self, request):
        user_account = request.POST["confirmdelete"]

        # User account is either email, or 'donotdelete' if the confirmation box isn't checked
        # Edit account is the name of the account regardless in order to autofill form if submitted without check off
        account_to_edit = request.POST["editaccount"]
        account_to_edit = UserAccount.objects.get(user__email=account_to_edit)
        account = UserAccount.objects.get(user__id=request.user.id)

        # Confirmation box not checked
        if user_account == "donotdelete":
            return render(request, "deleteuser.html", {
                "message": "Must check box to confirm",
                "status": "error",
                "account": account,
                "editaccount": account_to_edit
            })
        else:
            # Delete user and its Django user account
            account_to_delete = UserAccount.objects.get(user__username=user_account)
            account_to_delete.user.delete()
            account_to_delete.delete()
            return redirect("/accounts", {
                "message": "User deleted successfully",
                "status": "success",
                "account": account,
                "accounts": UserAccount.objects.order_by("type"),
            })
