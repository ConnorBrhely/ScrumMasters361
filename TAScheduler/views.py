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
        validEmail = validate.validate_email(email)
        password = request.POST["password"]
        secondpassword = request.POST["confirmpassword"]
        try:
            equalPassword = (password == secondpassword)
            validPassword = validate.validate_password(password)
            m = User.objects.get(email=email)
        except:
            noSuchUser = True
        if noSuchUser and validPassword and equalPassword and validEmail:
            m = User.objects.register(name="ben", email=email, password=password, user_type=request.POST["type"])
            m.save()
            return render(request, "createuser.html", {"message": "User successfully created"})
        elif not equalPassword:
            return render(request, "createuser.html", {"message": "Passwords do not match"})
        elif not validPassword:
            return render(request, "createuser.html", {"message": "Passwords does not contain 8 characters with 1 uppercase letter and 1 number"})
        else:
            return render(request, "createuser.html", {"message": "User with email already exists"})
