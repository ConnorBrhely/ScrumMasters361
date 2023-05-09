from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from TAScheduler.models import UserAccount

@login_required
def home_view(request):
    account = UserAccount.objects.get(user=request.user)
    message = None
    status = None

    if request.method == 'POST':
        # Handle any post requests here
        pass

    return render(request, 'home.html', {
        'account': account,
        'message': message,
        'status': status
    })
