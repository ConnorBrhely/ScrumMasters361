from django.shortcuts import render, redirect
from django.views import View
from TAScheduler.models import UserAccount
from django.contrib.auth.hashers import check_password
from django.core.exceptions import PermissionDenied
from ..common import validate

class ModifyAccount(View):
    def get(self, request):
        account = UserAccount.objects.get(user_id=request.user.id)
        if not request.user.is_authenticated:
            return redirect("/login")
        if request.GET["username"] != account.user.username:
            raise PermissionDenied

        return render(request, "modifyaccount.html", {
            "account": account,
        })

    def post(self, request):
        account = UserAccount.objects.get(user_id=request.user.id)

        phone_number = request.POST["phone"].strip()
        address = request.POST["address"].strip()
        email = request.POST["email"].strip() if account.type == "ADMIN" else ""
        office_hours = request.POST["officehours"].strip()
        password = request.POST["password"].strip()

        if not check_password(password, account.user.password):
            return self.render_error(request, account, "Incorrect password")

        if len(phone_number) > 0:
            if not validate.phone_number(phone_number):
                return self.render_error(request, account, "Invalid phone number")
            account.phone_number = phone_number
        if len(address) > 0:
            if not validate.address(address):
                return self.render_error(request, account, "Invalid address")
            account.home_address = address
        if len(email) > 0 and account.user.email != email:
            if not validate.email(email):
                return self.render_error(request, account, "Invalid email address")
            account.user.email = email
        if len(office_hours) > 0:
            if not validate.office_hours(office_hours):
                return self.render_error(request, account, "Invalid office hours")
            account.office_hours = office_hours

        account.save()
        return self.render_success(request, account, "Updated account information")

    @staticmethod
    def render_success(request, account, message):
        return render(request, "modifyaccount.html", {
            "account": account,
            "message": message,
            "status": "success"
        })

    @staticmethod
    def render_error(request, account, message):
        return render(request, "modifyaccount.html", {
            "account": account,
            "message": message,
            "status": "error"
        })