from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.shortcuts import render



# Create your views here.

@login_required
def profile(request, pk=None):
    if pk:
        u = User.objects.get(id=pk)
        user = u
    else:
        user = request.user
    return render(request, 'accounts/profile.html', {'user': user})



