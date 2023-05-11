from django.shortcuts import render, redirect
from django.views import View
from TAScheduler.models import UserAccount, Section


class Sections(View):
    def get(self, request):
        account = UserAccount.objects.get(user_id=request.user.id)
        sections = Section.objects.order_by("course")
        return render(request, "sections.html", {"sections": sections, "account": account})

    def post(self, request):
        account = UserAccount.objects.get(user_id=request.user.id)
        section_to_delete = request.POST.get("delete")
        if section_to_delete is not None:
            Section.objects.get(id=section_to_delete).delete()
            return redirect("/sections")
        sort_method = request.POST["sorttype"].strip()
        if sort_method == "number" or sort_method == "numberreverse":
            sections = Section.objects.order_by("number")
            if sort_method == "numberreverse":
                sections = sections.reverse()
        elif sort_method == "location" or sort_method == "locationreverse":
            sections = UserAccount.objects.order_by("location")
            if sort_method == "locationreverse":
                sections = sections.reverse()
        else:
            sections = UserAccount.objects.order_by("course")
        return render(request, "sections.html", {"sections": sections, "account": account})
