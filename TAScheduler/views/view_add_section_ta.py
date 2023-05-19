from django.shortcuts import render, redirect
from django.views import View
from TAScheduler.common import validate
from TAScheduler.models import UserAccount, Section


class AddSectionTA(View):
    def post(self, request):
        # User must be logged in to add a TA to a section
        if not request.user.is_authenticated:
            return redirect("/login")

        # User must be an admin/instructor to add a TA to a section
        account = UserAccount.objects.get(user_id=request.user.id)
        if account.type != UserAccount.UserType.ADMIN or account.type != UserAccount.UserType.INSTRUCTOR:
            return redirect("/")

        section_id = request.POST["section_id"]
        section = Section.objects.get(pk=section_id)
        ta_to_add = UserAccount.objects.get(pk=request.POST["ta-to-add"])

        # User should never be able to add a TA that is already in the section in normal operation, but just in case
        if ta_to_add not in section.get_tas():
            section.add_ta(ta_to_add)

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