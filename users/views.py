from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import UserEditForm

def user_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        if 'edit_user' in request.POST:  # Handle Edit Form
            form = UserEditForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
                messages.success(request, "User updated successfully!")
                return redirect('user_profile', user_id=user.id)
        elif 'delete_user' in request.POST:  # Handle Delete
            user.delete()
            messages.success(request, "User deleted successfully!")
            return redirect('user_list')  # Redirect to user list after deletion
    else:
        form = UserEditForm(instance=user)

    return render(request, 'users/user_profile.html', {'form': form, 'user': user})
