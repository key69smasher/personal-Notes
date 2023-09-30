from django.shortcuts import render,redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

def register(request):
    """Register a new user"""
    if request.method != 'POST':
        # Display the blank registration form
        form = UserCreationForm()
    else:
        form = UserCreationForm(data=request.POST)

        if form.is_valid():
            new_user=form.save()
            login(request,new_user)
            # this login function provide seprate session for the new user
            return redirect('learning_logs:index')
        
    context={'form': form}
    return render(request, 'registration/register.html', context)
