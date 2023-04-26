from django.shortcuts import render, redirect
from django.views import View
from TAScheduler.common import validate
from TAScheduler.models import UserAccount


class CreateUser(View):
    def get(self, request):
        return render(request, "createuser.html", {})

    def post(self, request):
        first_name = request.POST["firstname"]
        last_name = request.POST["lastname"]
        email = request.POST["email"]
        email_valid = validate.validate_email(email)
        if not email_valid:
            return render(request, "createuser.html", {"message": "Invalid email entered"})

        password = request.POST["password"]
        confirm_password = request.POST["confirmpassword"]

        if email == "" \
                or password == "" \
                or confirm_password == "" \
                or first_name == "" \
                or last_name == "":
            return render(request, "createuser.html", {"message": "One or more blank field detected"})

        password_equal = (password == confirm_password)
        password_valid = validate.validate_password(password)

        no_such_user = False
        try:
            UserAccount.objects.get(user__email=email)
        except UserAccount.DoesNotExist:
            no_such_user = True
        if no_such_user and password_valid and password_equal:
            m = UserAccount.objects.register(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password,
                user_type=request.POST["type"]
            )
            m.save()
            return render(request, "createuser.html", {"message": "User successfully created"})
        elif not password_equal:
            return render(request, "createuser.html", {"message": "Passwords do not match"})
        elif not password_valid:
            return render(request, "createuser.html",
                          {"message": "Password does not contain 8 characters with 1 uppercase letter and 1 number"})
        else:
            return render(request, "createuser.html", {"message": "User with email already exists"})
