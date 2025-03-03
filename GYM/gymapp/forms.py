from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Feedback,EatingPlan, DietingPlan, DailyProgress


class RegistrationForm(UserCreationForm):
    phone_number = forms.CharField(max_length=15)
    height = forms.FloatField()
    weight = forms.FloatField()

    class Meta:
        model = User
        fields = ['username', 'phone_number', 'height', 'weight', 'password1', 'password2']

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={
                'class': 'message-field form-control',  
                'rows': 2,  
                'aria-label': 'Feedback message',  
            }),
        }

    def __init__(self, *args, **kwargs):
        super(FeedbackForm, self).__init__(*args, **kwargs)
        self.fields['message'].label = 'Feedback Message' 

class EatingPlanForm(forms.ModelForm):
    class Meta:
        model = EatingPlan
        fields = ['date', 'meal_plan']

class DietingPlanForm(forms.ModelForm):
    class Meta:
        model = DietingPlan
        fields = ['date', 'plan_details']

class DailyProgressForm(forms.ModelForm):
    class Meta:
        model = DailyProgress
        fields = ['date', 'weight', 'body_fat_percentage', 'notes']
        
