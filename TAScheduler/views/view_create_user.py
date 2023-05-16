from django.shortcuts import render, redirect
from django.views import View
from TAScheduler.common import validate
from TAScheduler.models import UserAccount
from django.core.exceptions import PermissionDenied


class CreateUser(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect("/login")
        account = UserAccount.objects.get(user_id=request.user.id)
        if account.type != UserAccount.UserType.ADMIN:
            raise PermissionDenied
        return self.render_simple(request)

    def post(self, request):
        first_name = request.POST["firstname"].strip()
        last_name = request.POST["lastname"].strip()
        email = request.POST["email"].strip()

        if not validate.email(email):
            return self.render_simple(request, "Invalid email entered", "error")

        password = request.POST["password"].strip()
        confirm_password = request.POST["confirmpassword"].strip()

        if email == "" \
                or password == "" \
                or confirm_password == "" \
                or first_name == "" \
                or last_name == "":
            return self.render_simple(request, "One or more blank field detected", "error")

        password_equal = (password == confirm_password)
        password_valid = validate.password(password)

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
        elif not password_equal:
            return self.render_simple(request, "Passwords do not match", "error")
        elif not password_valid:
            return self.render_simple(request, "Password must contain 8 characters with 1 uppercase letter, 1 number, "
                                               "and 1 special character", "error")
        else:
            return self.render_simple(request, "User already exists", "error")

        return redirect("/accounts", {
            "message": "Account successfully created",
            "status": "success",
            "account": UserAccount.objects.get(user_id=request.user.id),
            "accounts": UserAccount.objects.order_by("type")
        })

    @staticmethod
    def render_simple(request, message="", status="success"):
        return render(request, "createuser.html", {
            "message": message,
            "status": status,
            "account": UserAccount.objects.get(user_id=request.user.id)
        })
