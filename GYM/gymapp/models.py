from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


# Extend the User model with additional fields
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    height = models.FloatField()
    weight = models.FloatField()

    def __str__(self):
        return self.user.username

class Course(models.Model):
    DURATION_CHOICES = [
        ('6 months', '6 Months'),
        ('1 year', '1 Year'),
        ('2 years', '2 Years'),
    ]
    duration = models.CharField(max_length=10, choices=DURATION_CHOICES)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.duration
    
class Membership(models.Model):
    duration = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.duration} - ₹{self.price}"

class Trainer(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    category = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='trainers')

    def __str__(self):
        return self.name

class TimeSlot(models.Model):
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.trainer.name} - {self.date} {self.time}"

class DailyClass(models.Model):
    date = models.DateField()
    workout_type = models.CharField(max_length=100)
    video_url = models.URLField(max_length=200)
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.workout_type} on {self.date}"


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    timeslot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(default=now)  # ✅ Fix: Uses now() correctly
    payment_status = models.BooleanField(default=False)
    class_assigned = models.ForeignKey(DailyClass, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"Booking {self.id} by {self.user} on {self.booking_date}"
    
class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    admin_reply = models.TextField(blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    replied_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Feedback from {self.user.username}"
    
class EatingPlan(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)  # Make user nullable

    MEAL_CHOICES = [
        ('Breakfast', 'Breakfast'),
        ('Lunch', 'Lunch'),
        ('Dinner', 'Dinner'),
    ]
    date = models.DateField()
    meal_plan = models.TextField()
    meal_type = models.CharField(max_length=10, choices=MEAL_CHOICES, default='Breakfast')

    def __str__(self):
        return f"{self.meal_type} on {self.date}"

class DietingPlan(models.Model):
    date = models.DateField()
    plan_details = models.TextField()

    def __str__(self):
        return f"Dieting Plan for {self.date}"

class DailyProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    weight = models.FloatField()
    body_fat_percentage = models.FloatField()
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Progress for {self.date} by {self.user.username}"