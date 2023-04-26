from django.shortcuts import render, redirect
from django.views import View
from TAScheduler.common import validate
from TAScheduler.models import UserAccount
from django.core.exceptions import PermissionDenied


class CreateUser(View):
    def get(self, request):
        account = UserAccount.objects.get(user_id=request.user.id)
        if not request.user.is_authenticated:
            return redirect("/login")
        if account.type != UserAccount.UserType.ADMIN:
            raise PermissionDenied
        return render(request, "createuser.html", {
            "account": account,
        })

    def post(self, request):
        first_name = request.POST["firstname"]
        last_name = request.POST["lastname"]
        email = request.POST["email"]
        email_valid = validate.validate_email(email)
        if not email_valid:
            return render(request, "createuser.html", {
                "message": "Invalid email entered",
                "account": UserAccount.objects.get(user_id=request.user.id),
            })

        password = request.POST["password"]
        confirm_password = request.POST["confirmpassword"]

        if email == "" \
                or password == "" \
                or confirm_password == "" \
                or first_name == "" \
                or last_name == "":
            return render(request, "createuser.html", {
                "message": "One or more blank field detected",
                "account": UserAccount.objects.get(user_id=request.user.id),
            })

        password_equal = (password == confirm_password)
        password_valid = validate.validate_password(password)

        no_such_user = False
        try:
            UserAccount.objects.get(user__email=email)
        except UserAccount.DoesNotExist:
            no_such_user = True

        message = None
        status = "success"

        if no_such_user and password_valid and password_equal:
            m = UserAccount.objects.register(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password,
                user_type=request.POST["type"]
            )
            m.save()
            message = "User successfully created"
        elif not password_equal:
            message = "Passwords do not match"
            status = "failure"
        elif not password_valid:
            message = "Password must contain 8 characters with 1 uppercase letter, 1 number, and 1 special character"
            status = "failure"
        else:
            message = "User with email already exists"
            status = "failure"

        return render(request, "createuser.html", {
            "message": message,
            "status": status,
            "account": UserAccount.objects.get(user_id=request.user.id),
        })
