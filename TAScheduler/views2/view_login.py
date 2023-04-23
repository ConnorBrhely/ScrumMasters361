from django.shortcuts import render, redirect
from django.views import View
from TAScheduler.models import User
from TAScheduler.common import validate

class Login(View):
    def get(self,request):
        return render(request, "Form.html", {})
    def post(self,request):
        noSuchUser = False
        badPassword = False
        try:
            m = User.objects.get(email = request.POST["email"])
            badPassword = (m.password != request.POST["password"])
        except:
            noSuchUser = True;

        if noSuchUser:
            m = User.objects.register(email = request.POST["email"], password = request.POST["password"])
            m.save()
            request.session["email"] = m.email
            return redirect("/home/")
        elif badPassword:
            return render(request,"Form.html", {"message":"incorrect password"})
        else:
            request.session["email"] = m.email
            return redirect("/home/")