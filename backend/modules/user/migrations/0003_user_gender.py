# Generated by Django 4.2.3 on 2023-07-19 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modules_user', '0002_alter_user_managers'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='gender',
            field=models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female')], max_length=2, null=True),
        ),
    ]
