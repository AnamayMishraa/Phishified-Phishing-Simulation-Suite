from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from .models import Profile, Team, Target
from django.contrib import messages
from .forms import TargetForm, TargetUploadForm
import csv

@login_required
def dashboard_home(request):
    return render(request, 'dashboard/dashboard.html')



@login_required
def profile(request):  # <-- Change function name
    profile = request.user.profile  # Fetch the logged-in user's profile

    if request.method == "POST":
        # Update Profile
        if "update_profile" in request.POST:
            name = request.POST.get("name")
            password = request.POST.get("password")

            if name:
                request.user.first_name, request.user.last_name = name.split(" ", 1) if " " in name else (name, "")
                request.user.save()

            if password:
                request.user.set_password(password)
                request.user.save()
                update_session_auth_hash(request, request.user)  # Keep user logged in

            return redirect("profile")

        # Leave Team
        if "leave_team" in request.POST:
            profile.team = None
            profile.save()
            return redirect("profile")

        # Join Team
        if "join_team" in request.POST:
            team_id = request.POST.get("team_id")
            team = Team.objects.get(id=team_id)
            profile.team = team
            profile.save()
            return redirect("profile")

    teams = Team.objects.all()
    return render(request, "dashboard/profile.html", {"profile": profile, "teams": teams})




@login_required
def teams(request):
    user = request.user
    user_team = None
    team_members = []

    if hasattr(user.profile, 'team') and user.profile.team:
        user_team = user.profile.team  
        team_members = user_team.members.all()

    if request.method == "POST":

         # Deleting a team (Only the leader can delete)
        if "delete_team" in request.POST:
            if user_team and user == user_team.leader:
                team_name = user_team.name
                user_team.delete()
                messages.success(request, f"Team '{team_name}' has been deleted.")
                return redirect("teams")

        # Creating a new team
        if "create_team" in request.POST:
            team_name = request.POST.get("team_name")

            # Check if the team name already exists
            if Team.objects.filter(name=team_name).exists():
                messages.error(request, "A team with this name already exists. Please choose a different name.")
            else:
                new_team = Team.objects.create(name=team_name, leader=user)
                new_team.members.add(user)  # Add creator to the team
                user.profile.team = new_team
                user.profile.save()
                messages.success(request, f"Team '{team_name}' created successfully!")
                return redirect("teams")

        # Leaving a team
        if "leave_team" in request.POST:
            if user.profile.team:
                user.profile.team.members.remove(user)
                user.profile.team = None
                user.profile.save()
                messages.success(request, "You have left the team.")
                return redirect("teams")

    return render(request, "dashboard/teams.html", {
        "user_team": user_team,
        "team_members": team_members,
    })


def targets(request):
    query = request.GET.get('search', '')  # Capture search query
    targets = Target.objects.all()  # Fetch all targets

    if query:
        targets = targets.filter(name__icontains=query)  

    if request.method == 'POST':
        if 'add_target' in request.POST:  # Manual Entry
            form = TargetForm(request.POST)
            if form.is_valid():
                target = form.save(commit=False)

                user = User.objects.filter(email=target.email).first()
                if user:
                    target.user = user  # Link Target to the User
                
                target.save()
                messages.success(request, "Target added successfully!")
                return redirect('targets')

        elif 'upload_targets' in request.POST:  # CSV Upload
            upload_form = TargetUploadForm(request.POST, request.FILES)
            if upload_form.is_valid():
                file = request.FILES['file']
                decoded_file = file.read().decode('utf-8').splitlines()
                csv_reader = csv.reader(decoded_file)
                next(csv_reader)  # Skip header row
                for row in csv_reader:
                    name, email, department = row
                    Target.objects.get_or_create(name=name, email=email, department=department)
                messages.success(request, "Targets uploaded successfully!")
                return redirect('targets')

    else:
        form = TargetForm()
        upload_form = TargetUploadForm()

    targets = Target.objects.all()  # Fetch all targets
    return render(request, 'dashboard/targets.html', {
        'form': form,
        'upload_form': upload_form,
        'targets': targets,
        'query': query
    })

    

def targets_view(request):
    query = request.GET.get('search', '')  # Get search query
    targets = Target.objects.all()

    if query:
        targets = targets.filter(name__icontains=query)  # Case-insensitive search

    return render(request, 'dashboard/targets.html', {'targets': targets, 'query': query})


@login_required
def campaigns(request):
    return render(request, 'dashboard/campaigns.html')

