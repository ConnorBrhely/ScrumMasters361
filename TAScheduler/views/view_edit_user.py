from django.shortcuts import render, redirect
from django.views import View
from TAScheduler.common import validate
from TAScheduler.models import UserAccount
from django.core.exceptions import PermissionDenied


class EditUser(View):

    def get(self, request):
        autofill = request.GET.get("username")
        try:
            account = UserAccount.objects.get(user_id=request.user.id)
            # If no username specified, redirect user to their own edit page
            if autofill is None:
                return redirect(f"/edit_user/?username={account.user.username}")
            if not request.user.is_authenticated:
                return redirect("/login")
            if account.type != UserAccount.UserType.ADMIN:
                raise PermissionDenied
            return self.render_simple(request)
        except UserAccount.DoesNotExist:
            raise PermissionDenied

    def post(self, request):
        username = request.GET["username"]
        first_name = request.POST["firstname"].strip()
        last_name = request.POST["lastname"].strip()
        email = request.POST["email"].strip()
        account = UserAccount.objects.get(user__username=username)

        if not validate.email(email):
            return self.render_simple(request, "Invalid email entered", "error")

        if not validate.name(first_name, last_name):
            return self.render_simple(request, "Invalid first or last name entered", "error")

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
            return self.render_simple(request, "One or more blank field detected", "error")

        password_equal = (password == confirm_password)
        password_valid = validate.password(password)
        same_email = False

        # Checks to see if the email changed
        if username == email:
            same_email = True

        """(If a user doesnt exist with new email or the same email is used) AND ((Password is valid and the two passwords
        entered are equal) OR (The length of both passwords fields are empty meaning no change)) Then update account"""
        if (no_such_user or same_email) and ((password_valid and password_equal) or (len(password) == 0 and len(confirm_password) == 0)):
            if password_valid and password_equal:
                account.update_password(password)
            account.update_email(email)
            account.update_name(first_name, last_name)
            return redirect("/accounts/", {
                "message": "User edited successfully",
                "status": "success",
                "account": UserAccount.objects.get(user_id=request.user.id),
                "accounts": UserAccount.objects.order_by("type")
            })
        elif not password_equal:
            return self.render_simple(request, "Passwords do not match", status="error")
        elif len(password) != 0 and not password_valid:
            return self.render_simple(request,
                                      "Password must contain 8 characters with 1 uppercase letter, 1 number, and 1 "
                                      "special character", status="error")
        else:
            return self.render_simple(request, "Account with email already exists", status="error")

    @staticmethod
    def render_simple(request, message="", status="success"):
        username = request.GET["username"]
        account_to_edit = UserAccount.objects.get(user__username=username)
        return render(request, "edituser.html", {
            "message": message,
            "status": status,
            "account": UserAccount.objects.get(user_id=request.user.id),
            "editaccount": account_to_edit
        })