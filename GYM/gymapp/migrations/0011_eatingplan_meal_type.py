# Generated by Django 5.1.1 on 2024-10-27 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gymapp', '0010_remove_dietingplan_user_remove_eatingplan_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='eatingplan',
            name='meal_type',
            field=models.CharField(choices=[('Breakfast', 'Breakfast'), ('Lunch', 'Lunch'), ('Dinner', 'Dinner')], default='Breakfast', max_length=10),
        ),
    ]
