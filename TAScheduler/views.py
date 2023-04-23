# Recreated the original views.py because trying to import and use the new separate
# views files for the urls was a bit of a pain.

from django.shortcuts import render, redirect
from django.views import View
from TAScheduler.models import User, Section
from TAScheduler.common import validate


class CreateUser(View):

    def get(self, request):
        return render(request, "createuser.html", {})

    def post(self, request):
        noSuchUser = False
        name = request.POST["name"]
        email = request.POST["email"]
        validEmail = validate.validate_email(email)
        if not validEmail:
            return render(request, "createuser.html", {"message": "Invalid email entered"})
        password = request.POST["password"]
        secondpassword = request.POST["confirmpassword"]
        if email == "" or password == "" or secondpassword == "" or name == "":
            return render(request, "createuser.html", {"message": "One or more blank field detected"})
        try:
            equalPassword = (password == secondpassword)
            validPassword = validate.validate_password(password)
            m = User.objects.get(email=email)
        except:
            noSuchUser = True
        if noSuchUser and validPassword and equalPassword:
            m = User.objects.register(name=name, email=email, password=password, user_type=request.POST["type"])
            m.save()
            return render(request, "createuser.html", {"message": "User successfully created"})
        elif not equalPassword:
            return render(request, "createuser.html", {"message": "Passwords do not match"})
        elif not validPassword:
            return render(request, "createuser.html",
                          {"message": "Passwords does not contain 8 characters with 1 uppercase letter and 1 number"})
        else:
            return render(request, "createuser.html", {"message": "User with email already exists"})


class Login(View):
    def get(self, request):
        return render(request, "Form.html", {})

    def post(self, request):
        noSuchUser = False
        badPassword = False
        try:
            m = User.objects.get(email=request.POST["email"])
            badPassword = (m.password != request.POST["password"])
        except:
            noSuchUser = True;

        if noSuchUser:
            m = User.objects.register(email=request.POST["email"], password=request.POST["password"])
            m.save()
            request.session["email"] = m.email
            return redirect("/home/")
        elif badPassword:
            return render(request, "Form.html", {"message": "incorrect password"})
        else:
            request.session["email"] = m.email
            return redirect("/home/")


class Home(View):
    def get(self, request):
        return render(request, "home.html", {})

    # def post(self, request):


class CreateSection(View):
    def get(self, request):
        return render(request, "createsection.html", {})

    def post(self, request):
        noSuchSection = False
        course = request.POST["course"]
        name = request.POST["name"]
        location = request.POST["location"]

        if course == "" or name == "" or location == "":
            return render(request, "createsection.html", {"message": "One or more blank field detected"})
        try:
            m = Section.objects.get(name=name)
        except:
            noSuchSection = True
        if noSuchSection:
            # m = User.objects.register(course=course, name=name, location=location)
            m = Section()
            m.course = course
            m.name = name
            m.location = location
            m.save()
            return render(request, "createsection.html", {"message": "Section successfully created"})
        else:
            return render(request, "createsection.html", {"message": "Section already exists"})
