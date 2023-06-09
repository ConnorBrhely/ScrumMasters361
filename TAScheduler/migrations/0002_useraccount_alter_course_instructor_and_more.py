# Generated by Django 4.1.7 on 2023-04-24 02:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("TAScheduler", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="UserAccount",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("first_name", models.CharField(max_length=128)),
                ("last_name", models.CharField(max_length=128)),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("TA", "TA"),
                            ("PROFESSOR", "Professor"),
                            ("ADMIN", "Admin"),
                        ],
                        max_length=32,
                    ),
                ),
                (
                    "home_address",
                    models.CharField(blank=True, max_length=256, null=True),
                ),
                (
                    "phone_number",
                    models.CharField(blank=True, max_length=16, null=True),
                ),
                (
                    "office_hours",
                    models.CharField(blank=True, max_length=256, null=True),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AlterField(
            model_name="course",
            name="instructor",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="instructor",
                to="TAScheduler.useraccount",
            ),
        ),
        migrations.AlterField(
            model_name="section",
            name="tas",
            field=models.ManyToManyField(
                related_name="sections", to="TAScheduler.useraccount"
            ),
        ),
        migrations.DeleteModel(
            name="User",
        ),
    ]
