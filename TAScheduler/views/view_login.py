from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views import View
from TAScheduler.models import UserAccount

class Login(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("/home/")
        return render(request, "login.html", {})

    def post(self,request):
        if "email" not in request.POST or request.POST["email"] == "":
            return render(request, "login.html", {
                "message": "No email provided",
                "status": "error",
            })
        if "password" not in request.POST or request.POST["password"] == "":
            return render(request, "login.html", {
                "message": "No password provided",
                "status": "error",
            })

        email = request.POST["email"].strip()
        password = request.POST["password"].strip()

        if UserAccount.objects.count() == 0:
            m = UserAccount.objects.register(
                first_name="Admin",
                last_name="User",
                email=email,
                password=password,
                user_type=UserAccount.UserType.ADMIN
            )
            m.user.is_superuser = True
            login(request, m.user)
            return redirect("/home/", {
                "message": "Initial admin user created",
                "status": "info",
            })

        m = authenticate(username=email, password=password)

        if m is not None:
            login(request, m)
            return redirect("/home/")
        else:
            return render(request, "login.html", {
                "message": "Invalid email or password",
                "status": "error",
            })
