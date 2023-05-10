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
        return render(request, "createuser.html", {"account": account})

    def post(self, request):
        first_name = request.POST["firstname"].strip()
        last_name = request.POST["lastname"].strip()
        email = request.POST["email"].strip()

        if not validate.email(email):
            return render(request, "createuser.html", {
                "message": "Invalid email entered",
                "account": UserAccount.objects.get(user_id=request.user.id),
            })

        password = request.POST["password"].strip()
        confirm_password = request.POST["confirmpassword"].strip()

        if email == "" \
                or password == "" \
                or confirm_password == "" \
                or first_name == "" \
                or last_name == "":
            return render(request, "createuser.html", {
                "message": "One or more blank field detected",
                "status": "error",
                "account": UserAccount.objects.get(user_id=request.user.id),
            })

        password_equal = (password == confirm_password)
        password_valid = validate.password(password)

        no_such_user = False
        try:
            UserAccount.objects.get(user__email=email)
        except UserAccount.DoesNotExist:
            no_such_user = True

        message = "User successfully created"
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
        elif not password_equal:
            message = "Passwords do not match"
            status = "error"
            return render(request, "createuser.html", {
                "message": message,
                "status": status,
                "account": UserAccount.objects.get(user_id=request.user.id),
            })
        elif not password_valid:
            message = "Password must contain 8 characters with 1 uppercase letter, 1 number, and 1 special character"
            status = "error"
            return render(request, "createuser.html", {
                "message": message,
                "status": status,
                "account": UserAccount.objects.get(user_id=request.user.id),
            })
        else:
            message = "User with email already exists"
            status = "error"
            return render(request, "createuser.html", {
                "message": message,
                "status": status,
                "account": UserAccount.objects.get(user_id=request.user.id),
            })

        return redirect("/accounts", {
            "message": message,
            "status": status,
            "account": UserAccount.objects.get(user_id=request.user.id),
            "accounts": UserAccount.objects.order_by("type")
        })
