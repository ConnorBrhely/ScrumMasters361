from django.shortcuts import render, redirect
from django.views import View
from TAScheduler.models import UserAccount, Section


class Sections(View):
    def get(self, request):
        # If user is not logged in, redirect to login page
        if not request.user.is_authenticated:
            return redirect("/login")

        # Sort sections by course by default
        account = UserAccount.objects.get(user_id=request.user.id)
        sections = Section.objects.order_by("course")
        return render(request, "sections.html", {"sections": sections, "account": account})

    def post(self, request):
        account = UserAccount.objects.get(user_id=request.user.id)
        section_to_delete = request.POST.get("delete")

        # If section_to_delete is not None, we are deleting a section
        if section_to_delete is not None:
            Section.objects.get(id=section_to_delete).delete()
            return redirect("/sections")

        # Sort sections based on sort_method
        sort_method = request.POST["sorttype"].strip()
        if sort_method  == "number":
            sections = Section.objects.order_by("number")
        elif sort_method == "numberreverse":
            sections = Section.objects.order_by("number").reverse()
        elif sort_method == "location":
            sections = Section.objects.order_by("location")
        elif sort_method == "locationreverse":
            sections = Section.objects.order_by("location").reverse()
        elif sort_method == "course":
            sections = Section.objects.order_by("course")
        else:
            # If sort_method is invalid, default to sorting by course and display error message
            sections = Section.objects.order_by("course")
            return render(request, "sections.html", {
                "sections": sections,
                "account": account,
                "sort_method": sort_method,
                "message": "Invalid sort method",
                "status": "error"
            })

        return render(request, "sections.html", {
            "sections": sections,
            "account": account,
            "sort_method": sort_method
        })
