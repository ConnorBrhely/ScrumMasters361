from django.shortcuts import render, redirect
from django.views import View
from TAScheduler.common import validate
from TAScheduler.models import UserAccount, Section


class AddSectionTA(View):
    def post(self, request):
        section_id = request.POST["section_id"]
        section = Section.objects.get(pk=section_id)
        print("Added TA to section " + section_id)
        return redirect("/edit_section?id=" + section_id)

    @staticmethod
    def render_simple(request, message="", status="success"):
        section_id = request.GET["id"]
        section_to_edit = Section.objects.get(pk=section_id)
        return render(request, "editsection.html", {
            "message": message,
            "status": status,
            "account": UserAccount.objects.get(user_id=request.user.id),
            "editsection": section_to_edit,
            "tas_in_section": section_to_edit.get_tas(),
            "tas": UserAccount.objects.filter(type=UserAccount.UserType.TA),
        })