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
        return render(request, "edituser.html", {"message": "hello there", "account": account, "editaccount": editaccount})

    def post(self, request):
        username = request.GET["username"]
        first_name = request.POST["firstname"].strip()
        last_name = request.POST["lastname"].strip()
        email = request.POST["email"].strip()
        account = UserAccount.objects.get(user__username=username)
        """Checks for valid email address"""
        if not validate.validate_email(email):
            return render(request, "edituser.html", {
                "message": "Invalid email entered",
                "account": UserAccount.objects.get(user_id=request.user.id),
                "editaccount": account
            })
        """Checks for valid first and last name"""
        if not validate.validate_name(first_name, last_name):
            return render(request, "edituser.html", {
                "message": "Invalid first or last name entered",
                "account": UserAccount.objects.get(user_id=request.user.id),
                "editaccount": account
            })
        """Checks if a user already exists with email they want to update too"""
        no_such_user = False
        try:
            UserAccount.objects.get(user__email=email)
        except UserAccount.DoesNotExist:
            no_such_user = True

        password = request.POST["password"].strip()
        confirm_password = request.POST["confirmpassword"].strip()
        """Checks for empty string fields and returns if so"""
        if email == "" \
                or first_name == "" \
                or last_name == "":
            return render(request, "edituser.html", {
                "message": "One or more blank field detected",
                "status": "failure",
                "account": UserAccount.objects.get(user_id=request.user.id),
                "editaccount": account
            })
        password_equal = (password == confirm_password)
        password_valid = validate.validate_password(password)
        message = "User edited successfully"
        status = "success"
        sameEmail = False
        """Checks to see if the email changed"""
        if username == email:
            sameEmail = True
        """(If a user doesnt exist with new email or the same email is used) AND ((Password is valid and the two passwords
        entered are equal) OR (The length of both passwords fields are empty meaning no change)) Then update account"""
        if (no_such_user or sameEmail) and ((password_valid and password_equal) or (len(password) == 0 and len(confirm_password) == 0)):
            if password_valid and password_equal:
                account.update_password(password)
            account.update_email(email)
            account.update_name(first_name, last_name)
            return redirect("/accounts/", {
                "message": message,
                "status": status,
                "account": UserAccount.objects.get(user_id=request.user.id),
                "accounts": UserAccount.objects.order_by("type")
            })
        elif not password_equal:
            message = "Passwords do not match"
            status = "failure"
            return render(request, "edituser.html", {
                "message": message,
                "status": status,
                "account": UserAccount.objects.get(user_id=request.user.id),
                "editaccount": account
            })
        elif len(password) != 0 and not password_valid:
            message = "Password must contain 8 characters with 1 uppercase letter, 1 number, and 1 special character"
            status = "failure"
            return render(request, "edituser.html", {
                "message": message,
                "status": status,
                "account": UserAccount.objects.get(user_id=request.user.id),
                "editaccount": account
            })
        else:
            message = "Account with email already exists"
            status = "failure"
            return render(request, "edituser.html", {
                "message": message,
                "status": status,
                "account": UserAccount.objects.get(user_id=request.user.id),
                "editaccount": account
            })
