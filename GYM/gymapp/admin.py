from django.contrib import admin
from .models import Profile, Course, Trainer, TimeSlot, Booking,DailyClass,Feedback,EatingPlan, DietingPlan, DailyProgress
from django.utils import timezone


from django import forms


class BookingAdminForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['user', 'course', 'trainer', 'timeslot', 'payment_status', 'class_assigned']

    class_assigned = forms.ModelChoiceField(
        queryset=DailyClass.objects.all(),
        required=False,
        label="Assign Class"
    )


class BookingAdmin(admin.ModelAdmin):
    form = BookingAdminForm
    list_display = ('user', 'course', 'trainer', 'payment_status', 'class_assigned')
    list_filter = ('payment_status', 'trainer', 'course')
    search_fields = ['user__username']

    def save_model(self, request, obj, form, change):
        # Logic for assigning class
        if form.is_valid():
            if obj.payment_status and form.cleaned_data['class_assigned']:
                obj.class_assigned = form.cleaned_data['class_assigned']
            super().save_model(request, obj, form, change)


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'admin_reply', 'submitted_at', 'replied_at')
    list_filter = ('submitted_at',)
    search_fields = ['user__username', 'message']

    def save_model(self, request, obj, form, change):
        if obj.admin_reply and not obj.replied_at:
            obj.replied_at = timezone.now()
        super().save_model(request, obj, form, change)

class EatingPlanAdmin(admin.ModelAdmin):
    list_display = ('date', 'meal_type', 'meal_plan', 'user')  # Added 'user'
    list_filter = ('meal_type', 'date')  # Filters by meal type and date
    search_fields = ('meal_plan',)
    ordering = ('-date',)  # Order by date descending
    date_hierarchy = 'date'  # Enable date drilling
    fieldsets = (
        (None, {
            'fields': ('user', 'date', 'meal_type', 'meal_plan')  # Customizing form layout
        }),
    )

admin.site.register(EatingPlan,EatingPlanAdmin)

admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(Profile)
admin.site.register(Course)
admin.site.register(Trainer)
admin.site.register(TimeSlot)
admin.site.register(Booking, BookingAdmin)
admin.site.register(DailyClass)

admin.site.register(DietingPlan)
admin.site.register(DailyProgress)