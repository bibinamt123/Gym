from django import forms
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse  # Use reverse for better redirect handling
from gymapp.models import Booking, Course, Trainer, Profile,Membership
from django.contrib import messages
from gymapp.models import Feedback
from django.contrib.auth.decorators import login_required
from datetime import datetime
from gymapp.models import Booking

def update_payment_status(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    booking.payment_status = True  # ✅ Mark as paid
    booking.save()
    messages.success(request, f"Payment for Booking {booking.id} updated to PAID!")
    return redirect('user_profiles')

def payment_success(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    booking.payment_status = True  # ✅ Mark as Paid
    booking.save()
    return JsonResponse({'success': True})


def delete_report(request, report_id):
    if request.method == "POST":
        report = get_object_or_404(report_a4, id=report_id)
        report.delete()
        return JsonResponse({"success": True})
    return JsonResponse({"success": False}, status=400)

# Trainer Form
class TrainerForm(forms.ModelForm):
    class Meta:
        model = Trainer
        fields = ['name', 'age', 'category', 'photo']

# View for listing user profiles, trainers, bookings, and courses

# @login_required
# def feedback_list_admin(request):
#     """View for admin to see all feedback from users."""
#     feedbacks = Feedback.objects.all()
#     return render(request, 'adminapp/feedback_list.html', {'feedbacks': feedbacks})

def reply_feedback(request, feedback_id):
    feedback = get_object_or_404(Feedback, id=feedback_id)
    
    if request.method == "POST":
        reply = request.POST.get("reply")
        feedback.admin_reply = reply
        feedback.save()
        return redirect('user_profiles')  # Redirect to an appropriate page

    return render(request, "adminapp/reply_feedback.html", {"feedback": feedback})

def delete_feedback(request, feedback_id):
    feedback = get_object_or_404(Feedback, id=feedback_id)
    feedback.delete()
    return redirect('user_profiles')  


def user_profiles(request):
    profiles = Profile.objects.all()
    trainers = Trainer.objects.all()
    bookings = Booking.objects.all()
    courses = Course.objects.all()
    feedbacks = Feedback.objects.all()



    # Debugging print (remove in production)
    for booking in bookings:
        print(f"Booking Date: {booking.booking_date}")  # Ensure date exists

    context = {
        'profiles': profiles,
        'trainers': trainers,
        'bookings': bookings,
        'courses': courses,
        'feedbacks': feedbacks

    }
    return render(request, 'adminapp/user_profiles.html', context)

# View for adding a trainer
def add_trainer(request):
    if request.method == "POST":
        form = TrainerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('user_profiles') + '#trainer-details')
    else:
        form = TrainerForm()
    return render(request, 'adminapp/add_trainer.html', {'form': form})

# View for deleting a trainer
def delete_trainer(request, trainer_id):
    trainer = get_object_or_404(Trainer, id=trainer_id)
    trainer.delete()
    return redirect('user_profiles')

# Admin login view
def admin_login(request):
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('user_profiles')
        else:
            error = "Invalid credentials. Please try again."

    return render(request, 'adminapp/login.html', {'error': error})

# def feedback_page(request):
#     feedbacks = Feedback.objects.all()  # Fetch all feedback entries
#     return render(request, "adminapp/user_profiles.html", {"feedbacks": feedbacks})

# Logout view
def logout_view(request):
    logout(request)
    return redirect('admin_login')  # Ensure 'admin_login' is a valid URL name

# View for membership details
def membership_details(request):
    courses = Membership.objects.all()
    return render(request, "adminapp/membership.html", {"courses": courses})

def add_membership(request):
    if request.method == "POST":
        duration = request.POST["duration"]
        price = request.POST["price"]
        
        Membership.objects.create(duration=duration, price=price)
        messages.success(request, "Membership plan added successfully!")
        return redirect("membership_details")

    return redirect("membership_details")

def delete_membership(request, membership_id):
    membership = get_object_or_404(Membership, id=membership_id)
    membership.delete()
    messages.success(request, "Membership plan deleted successfully!")
    return redirect("membership_details")

# View for generating report
def report_a4(request):
    bookings = Booking.objects.all().order_by('-booking_date')  # Sort by latest bookings
    context = {'bookings': bookings}
    return render(request, 'adminapp/report_pdf.html', context)

