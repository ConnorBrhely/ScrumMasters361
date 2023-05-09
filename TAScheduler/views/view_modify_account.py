from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from TAScheduler.models import UserAccount

@login_required
def personal_accounts_view(request):
    user_account = UserAccount.objects.get(user_id=request.user.id)

    if request.method == 'POST':
        # Handle updating user account information here
        pass

    return render(request, 'personal_accounts.html', {
        'user_account': user_account
    })
