from django.shortcuts import render
from django.views import View
from TAScheduler.models import User
from TAScheduler.common import validate


class CreateUser(View):

    def get(self, request):
        return render(request, "createuser.html", {})

    def post(self, request):
        noSuchUser = False
        validPassword = False
        equalPassword = False
        validEmail = False

        email = request.POST["email"]
        badEmail = validate.validate_email(email)
        password = request.POST["password"]
        secondpassword = request.POST["confirmpassword"]
        try:
            m = User.objects.get(email=email)
            equalPassword = (password == secondpassword)
            validPassword = validate.validate_password(password)
        except:
            noSuchUser = True
        if noSuchUser and validPassword and equalPassword and validEmail:
            m = User(email=email, password=password)
            m.save()
            return render(request, "createuser.html", {"message": "User successfully created"})
        elif not validPassword:
            return render(request, "createuser.html", {"message": "Passwords does not contain 8 characters with 1 uppercase letter and 1 number"})
        elif not equalPassword:
            return render(request, "createuser.html", {"message": "Passwords do not match"})
        else:
            return render(request, "createuser.html", {"message": "User with email already exists"})
