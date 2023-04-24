from django.shortcuts import render, redirect
from django.views import View
from TAScheduler.models import UserAccount

class Login(View):
    def get(self, request):
        return render(request, "login.html", {})
    def post(self,request):
        no_such_user = False
        bad_password = False
        try:
            m = UserAccount.objects.get(email = request.POST["email"])
            bad_password = (m.password != request.POST["password"])
        except:
            no_such_user = True;

        if no_such_user:
            m = UserAccount.objects.register(email = request.POST["email"], password = request.POST["password"])
            m.save()
            request.session["email"] = m.email
            return redirect("/home/")
        elif bad_password:
            return render(request,"Form.html", {"message":"incorrect password"})
        else:
            request.session["email"] = m.email
            return redirect("/home/")
