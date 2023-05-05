from django.shortcuts import render, redirect
from django.views import View
from TAScheduler.common import validate
from TAScheduler.models import UserAccount
from django.core.exceptions import PermissionDenied


class EditUser(View):

    def get(self, request):
        autofill = request.GET["username"]
        account = UserAccount.objects.get(user_id=request.user.id)
        editaccount = UserAccount.objects.get(user__username=autofill)
        if not request.user.is_authenticated:
            return redirect("/login")
        if account.type != UserAccount.UserType.ADMIN:
            raise PermissionDenied
        return render(request, "edituser.html", {"account": account, "editaccount": editaccount})

    def post(self, request):
        first_name = request.POST["firstname"].strip()
        last_name = request.POST["lastname"].strip()
        email = request.POST["email"].strip()
        account = UserAccount.objects.get(user__email=email)

        if not validate.validate_email(email):
            return render(request, "edituser.html", {
                "message": "Invalid email entered",
                "account": UserAccount.objects.get(user_id=request.user.id),
            })

        password = request.POST["password"].strip()
        confirm_password = request.POST["confirmpassword"].strip()
        if password == "" and password != confirm_password:
            return render(request, "edituser.html", {
                "message": "Passwords must both be blank or filled in",
                "status": "failure",
                "account": UserAccount.objects.get(user_id=request.user.id)
            })
        if email == "" \
                or first_name == "" \
                or last_name == "":
            print("One or more blank field detected")
            return render(request, "edituser.html", {
                "message": "One or more blank field detected",
                "status": "failure",
                "account": UserAccount.objects.get(user_id=request.user.id),
            })
        password_equal = (password == confirm_password)
        password_valid = validate.validate_password(password)
        message = "User edited successfully"
        status = "success"
        if password_valid and password_equal:
            account.update_password(password)
        elif not password_equal:
            message = "Passwords do not match"
            status = "failure"
            return render(request, "edituser.html", {
                "message": message,
                "status": status,
                "account": UserAccount.objects.get(user_id=request.user.id),
            })
        else:
            message = "Password must contain 8 characters with 1 uppercase letter, 1 number, and 1 special character"
            status = "failure"
            return render(request, "edituser.html", {
                "message": message,
                "status": status,
                "account": UserAccount.objects.get(user_id=request.user.id),
            })
        return render(request, "accounts.html", {
            "message": message,
            "status": status,
            "account": UserAccount.objects.get(user_id=request.user.id),
            "accounts": UserAccount.objects.order_by("type")
        })
