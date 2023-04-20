from django.shortcuts import render
from django.views import View
from TAScheduler.models import User


class CreateUser(View):

    def get(self, request):
        return render(request, "createuser.html", {})

    def post(self, request):
        noSuchUser = False
        badPassword = False

        email = request.POST["email"]
        password = request.POST["password"]
        secondpassword = request.POST["confirmpassword"]
        try:
            m = User.objects.get(email=email)
            badPassword = (password != secondpassword)
        except:
            noSuchUser = True
        if noSuchUser & badPassword == True:
            m = User(email=email, password=password)
            m.save()
            return render(request, "createuser.html", {"message": "User successfully created"})
        elif badPassword:
            return render(request, "createuser.html", {"message": "Passwords do not match"})
        else:
            return render(request, "createuser.html", {"message": "User with email already exists"})
