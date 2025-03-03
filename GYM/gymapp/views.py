from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required

from django.contrib.auth import authenticate, login, logout
from .forms import RegistrationForm, LoginForm,FeedbackForm,EatingPlanForm,DailyProgressForm,DietingPlanForm

from .models import Course, Trainer, TimeSlot, Booking,Profile,DailyClass,Feedback,EatingPlan, DietingPlan, DailyProgress
from django.http import HttpResponseBadRequest
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import datetime
from datetime import timedelta
from django.utils.timezone import now


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create a profile
            Profile.objects.create(
                user=user,
                phone_number=form.cleaned_data.get('phone_number'),
                height=form.cleaned_data.get('height'),
                weight=form.cleaned_data.get('weight')
            )
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                # Invalid credentials
                pass
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


def home(request):
    return render(request, 'home.html')

def course_list(request):
    courses = Course.objects.all()
    return render(request, 'course_list.html', {'courses': courses})

def trainer_list(request, course_id):
    trainers = Trainer.objects.all()
    request.session['course_id'] = course_id
    return render(request, 'trainer_list.html', {'trainers': trainers})

def timeslot_list(request, trainer_id):
    timeslots = TimeSlot.objects.filter(trainer_id=trainer_id, is_available=True)
    request.session['trainer_id'] = trainer_id
    return render(request, 'timeslot_list.html', {'timeslots': timeslots})

def payment(request, timeslot_id):
    timeslot = get_object_or_404(TimeSlot, id=timeslot_id)
    course = get_object_or_404(Course, id=request.session.get('course_id'))
    amount = int(course.price * 100)  # Razorpay accepts amounts in paise

    # Razorpay client setup
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

    # Create a Razorpay order
    payment = client.order.create({
        'amount': amount,  # Amount in paise
        'currency': 'INR',
        'payment_capture': '1'  # Auto capture payment
    })

    # Create booking entry but do not mark it as paid yet
    booking = Booking.objects.create(
        user=request.user,
        course=course,
        trainer=timeslot.trainer,
        timeslot=timeslot,
    )

    context = {
        'payment': payment,
        'booking': booking,
        'amount': amount / 100,  # Display amount in rupees
        'razorpay_key_id': settings.RAZORPAY_KEY_ID,
    }

    return render(request, 'payment.html', context)

@csrf_exempt
def payment_callback(request):
    if request.method == "POST":
        try:
            # Retrieve data from the POST request sent by Razorpay
            payment_id = request.POST.get('razorpay_payment_id')
            order_id = request.POST.get('razorpay_order_id')
            signature = request.POST.get('razorpay_signature')
            booking_id = request.POST.get('booking_id')

            # Verify the Razorpay signature
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
            params_dict = {
                'razorpay_order_id': order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
            client.utility.verify_payment_signature(params_dict)

            # If successful, update the booking status to paid
            booking = Booking.objects.get(id=booking_id)
            booking.payment_status = True
            booking.save()

            return render(request, 'payment_success.html', {'booking': booking})
         
        except Exception as e:
            return HttpResponseBadRequest(f"Payment failed: {e}")
    else:
        return HttpResponseBadRequest("Invalid request method.")
        return redirect('home')
    
def daily_class_view(request):
    # Check if the user has a paid booking
    booking = Booking.objects.filter(user=request.user, payment_status=True).first()

    if not booking:
        return render(request, 'no_access.html')  # No access if no paid booking

    if not booking.class_assigned:
        # If no class has been assigned, show a message
        return render(request, 'no_class_today.html', {'booking': booking})

    context = {
        'daily_class': booking.class_assigned,
        'booking': booking,
    }
    return render(request, 'daily_class.html', context)
    
def feedback_view(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.save()
            return redirect('feedback')
    else:
        form = FeedbackForm()
    
    feedbacks = Feedback.objects.filter(user=request.user)
    return render(request, 'feedback.html', {'form': form, 'feedbacks': feedbacks})

@staff_member_required
def admin_feedback_view(request):
    feedbacks = Feedback.objects.all()
    return render(request, 'admin_feedback.html', {'feedbacks': feedbacks})
    

def eating_plan_view(request):
        
    current_user = request.user
    breakfast_plans = EatingPlan.objects.filter(meal_type="Breakfast")
    lunch_plans = EatingPlan.objects.filter(meal_type="Lunch")
    dinner_plans = EatingPlan.objects.filter(meal_type="Dinner")

    context = {
        'breakfast_plans': breakfast_plans,
        'lunch_plans': lunch_plans,
        'dinner_plans': dinner_plans,
    }
    return render(request, 'eating_plan.html', context)


def dieting_plan_view(request):
    dieting_plans = DietingPlan.objects.all()  # All dieting plans
    return render(request, 'dieting_plan.html', {'dieting_plans': dieting_plans})

def daily_progress_view(request):
    progress_records = DailyProgress.objects.filter(user=request.user)
    return render(request, 'daily_progress.html', {'progress_records': progress_records})