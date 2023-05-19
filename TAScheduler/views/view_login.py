from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views import View
from TAScheduler.models import UserAccount

class Login(View):
    def get(self, request):
        # If user is already logged in, redirect to home page
        if request.user.is_authenticated:
            try:
                UserAccount.objects.get(user_id=request.user.id)
                if request.user.is_authenticated:
                    return redirect("/home/")
            except UserAccount.DoesNotExist:
                # User has no UserAccount object, so something went wrong during account creation
                return self.render_simple(request, "Your account was set up incorrectly. Please contact an administrator.", "error")

        return self.render_simple(request)

    def post(self,request):
        # Check if email and password are provided
        if "email" not in request.POST or request.POST["email"] == "":
            return self.render_simple(request, "No email provided", "error")
        if "password" not in request.POST or request.POST["password"] == "":
            return self.render_simple(request, "No password provided", "error")

        email = request.POST["email"].strip()
        password = request.POST["password"].strip()

        # First login creates admin user
        if UserAccount.objects.count() == 0:
            user = UserAccount.objects.register(
                first_name="Admin",
                last_name="User",
                email=email,
                password=password,
                user_type=UserAccount.UserType.ADMIN
            )
            user.user.is_superuser = True
            login(request, user.user)
            return redirect("/home/", {
                "message": "Initial admin user created",
                "status": "info",
            })

        user = authenticate(username=email, password=password)

        # User was authenticated
        if user is not None:
            login(request, user)
            return redirect("/home/")
        else:
            # Authentication failed
            return self.render_simple(request, "Invalid email or password", "error")

    @staticmethod
    def render_simple(request, message="", status=""):
        return render(request, "login.html", {
            "message": message,
            "status": status,
        })
