from django.shortcuts import render, redirect
from django.views import View
from TAScheduler.models import UserAccount
from django.contrib.auth.hashers import check_password
from django.core.exceptions import PermissionDenied
from ..common import validate

class ModifyAccount(View):
    def get(self, request):
        account = UserAccount.objects.get(user_id=request.user.id)

        # Redirect to login page if not logged in
        if not request.user.is_authenticated:
            return redirect("/login")

        # Don't let user modify an account that isn't theirs
        if request.GET["username"] != account.user.username:
            raise PermissionDenied

        return self.render_simple(request, account)

    def post(self, request):
        account = UserAccount.objects.get(user_id=request.user.id)

        phone_number = request.POST["phone"].strip()
        address = request.POST["address"].strip()
        email = request.POST["email"].strip() if account.type == "ADMIN" else ""
        office_hours = request.POST["officehours"].strip()
        password = request.POST["password"].strip()

        # Confirm that password is correct
        if not check_password(password, account.user.password):
            return self.render_simple(request, account, "Incorrect password", "error")

        # Validate and update account information
        if len(phone_number) > 0:
            if not validate.phone_number(phone_number):
                return self.render_simple(request, account, "Invalid phone number", "error")
            account.phone_number = phone_number
        if len(address) > 0:
            if not validate.home_address(address):
                return self.render_simple(request, account, "Invalid address", "error")
            account.home_address = address
        if len(email) > 0 and account.user.email != email:
            if not validate.email(email):
                return self.render_simple(request, account, "Invalid email address", "error")
            account.user.email = email
        if len(office_hours) > 0:
            if not validate.office_hours(office_hours):
                return self.render_simple(request, account, "Invalid office hours", "error")
            account.office_hours = office_hours

        account.save()
        return self.render_simple(request, account, "Updated account information")

    @staticmethod
    def render_simple(request, account, message="", status="success"):
        return render(request, "modifyaccount.html", {
            "account": account,
            "message": message,
            "status": status
        })