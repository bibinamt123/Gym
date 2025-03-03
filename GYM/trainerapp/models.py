from django.contrib.auth.models import User
from django.db import models

class Trainer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)  # Ensure `null=True` for now
    name = models.CharField(max_length=100)
    experience = models.IntegerField()
    specialization = models.CharField(max_length=200)

    def __str__(self):
        return self.name
class Workout(models.Model):
    name = models.CharField(max_length=200)
    duration = models.IntegerField()
    video = models.FileField(upload_to='workout_videos/', null=True, blank=True)

    def __str__(self):
        return self.name

class Workout(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    duration = models.CharField(max_length=50)
    intensity = models.CharField(max_length=50)

    def __str__(self):
        return self.title

class UserProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    calories_burned = models.IntegerField()
    workout_done = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.username} - {self.workout_done} - {self.calories_burned} kcal"

class MedicalHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    condition = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return f"{self.user.username} - {self.condition}"

class HealthTips(models.Model):
    trainer = models.ForeignKey(User, on_delete=models.CASCADE)
    tip = models.TextField()

    def __str__(self):
        return f"Tip by {self.trainer.username}"



