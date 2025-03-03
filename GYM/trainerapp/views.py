from pyexpat.errors import messages
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Workout, UserProgress, MedicalHistory, HealthTips,Trainer
from django.contrib.auth.models import User
@login_required
def trainer_dashboard(request):
    return render(request, 'app/trainer_dashboard.html')
def view_users(request):
    users = User.objects.all()  # Get all registered users
    return render(request, 'app/view_users.html', {'users': users})
def trainer_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')  # Use `.get()` to avoid the error
        password = request.POST.get('password', '')

        if username and password:  # Ensure both fields are filled
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('trainer_dashboard')  # Redirect to trainer dashboard
            else:
                return render(request, 'app/trainer_login.html', {'error': 'Invalid credentials'})
        else:
            return render(request, 'app/trainer_login.html', {'error': 'Both fields are required'})

    return render(request, 'app/trainer_login.html')


@login_required
def manage_workouts(request):
    try:
        trainer = Trainer.objects.get(user=request.user)  # Fetch trainer linked to user
        classes = DailyClass.objects.filter(trainer=trainer)  # Get only that trainer's classes
    except Trainer.DoesNotExist:
        trainer = None
        classes = []

    return render(request, 'app/manage_workouts.html', {'classes': classes})

@login_required
def track_progress(request):
    progress_data = UserProgress.objects.all()
    return render(request, 'trainerapp/track_progress.html', {'progress_data': progress_data})

@login_required
def view_medical_history(request):
    medical_records = MedicalHistory.objects.all()
    return render(request, 'trainerapp/view_medical_history.html', {'medical_records': medical_records})

@login_required
def health_tips(request):
    tips = HealthTips.objects.all()
    return render(request, 'trainerapp/health_tips.html', {'tips': tips})

@login_required
def trainer_logout(request):
    logout(request)
    return redirect('trainer_login')
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

def trainer_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:  # Ensure only trainers can log in
            login(request, user)
            return redirect('trainer_dashboard')
        else:
            return render(request, 'trainerapp/trainer_login.html', {'error': 'Invalid credentials'})
    return render(request, 'trainerapp/trainer_login.html')

def trainer_logout(request):
    logout(request)
    return redirect('trainer_login')
