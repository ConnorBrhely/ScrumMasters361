from django.shortcuts import render
from django.views import View
from TAScheduler.models import UserAccount
from TAScheduler.common import validate


class Home(View):
    def get(self,request):
        return render(request, "home.html", {})

    # def post(self, request):

