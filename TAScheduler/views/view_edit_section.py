from django.shortcuts import render, redirect
from django.views import View
from TAScheduler.common import validate
from TAScheduler.models import UserAccount, Section
from django.core.exceptions import PermissionDenied


class EditSection(View):
    def get(self, request):
        autofill = request.GET.get("id")
        try:
            account = UserAccount.objects.get(user_id=request.user.id)
            # If no username specified, redirect user to their own edit page
            if not request.user.is_authenticated:
                return redirect("/login")
            if account.type != UserAccount.UserType.ADMIN:
                raise PermissionDenied
            return self.render_simple(request)
        except UserAccount.DoesNotExist:
            raise PermissionDenied

    def post(self, request):
        number = request.POST["number"].strip()
        location = request.POST["location"].strip()
        time = request.POST["time"].strip()

        if not validate.section_number(number):
            return self.render_simple(request, "Invalid email entered", "error")
        if number == "" or location == "" or time == "":
            return self.render_simple(request, "One or more blank field detected", "error")

        section_id = request.POST["section_id"]
        section_to_edit = Section.objects.get(pk=section_id)

        section_to_edit.update_number(number)
        section_to_edit.update_location(location)
        section_to_edit.update_time(time)

        return self.render_simple(request, "Section successfully edited")

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