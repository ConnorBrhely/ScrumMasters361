from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.views import View

class Logout(View):
    def get(self, request):
        # Log out and redirect to login page
        logout(request)
        return redirect("/login")