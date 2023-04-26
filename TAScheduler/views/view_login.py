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
            return render(request, "login.html", {"message": "No email provided"})
        if "password" not in request.POST or request.POST["password"] == "":
            return render(request, "login.html", {"message": "No password provided"})

        if UserAccount.objects.count() == 0:
            m = UserAccount.objects.register(
                first_name="Admin",
                last_name="User",
                email=request.POST["email"],
                password=request.POST["password"],
                user_type=UserAccount.UserType.ADMIN
            )
            m.user.is_superuser = True
            print(authenticate(email=request.POST["email"], password=request.POST["password"]))
            request.session["email"] = m.user.email
            return redirect("/home/")

        password = request.POST["password"].strip()
        email = request.POST["email"].strip()

        m = authenticate(username=email, password=password)
        print(f"Email: \"{email}\"")
        print(f"Password: \"{password}\"")
        print("User: " + str(m))

        if m is not None:
            login(request, m)
            request.session["email"] = m.email
            return redirect("/home/")
        else:
            return render(request, "login.html", {"message": "Invalid email or password"})
