from django.urls import path
from . import views
from .views import admin_login, delete_feedback,logout_view, reply_feedback, update_payment_status

urlpatterns = [
    # This will match "/adminapp/" and render the user_profiles view
    path('', views.user_profiles, name='adminapp_home'),
    path('user_profiles/', views.user_profiles, name='user_profiles'),
    path('add_trainer/', views.add_trainer, name='add_trainer'),
    path('delete_trainer/<int:trainer_id>/', views.delete_trainer, name='delete_trainer'),
    path('membership/', views.membership_details, name='membership_details'),
    path("membership/add/", views.add_membership, name="add_membership"),
    path("membership/delete/<int:membership_id>/", views.delete_membership, name="delete_membership"),
    path('report_a4/', views.report_a4, name='report_a4'),
    path('login/', admin_login, name='admin_login'),  # Ensure this exists
    path('logout/', logout_view, name='admin_logout'),
    path('reply_feedback/<int:feedback_id>/', views.reply_feedback, name='reply_feedback'),
    path('delete-feedback/<int:feedback_id>/', delete_feedback, name='delete_feedback'),
    path('delete-report/<int:report_id>/', views.delete_report, name='delete_report'),
    path('update-payment/<int:booking_id>/', update_payment_status, name='update_payment_status'),



]
