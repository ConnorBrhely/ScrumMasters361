# Generated by Django 4.2.1 on 2023-05-10 00:51

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("TAScheduler", "0006_rename_name_section_number"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="course",
            name="term",
        ),
        migrations.AddField(
            model_name="course",
            name="term_season",
            field=models.CharField(
                choices=[("Fall", "Fall"), ("Spring", "Spring"), ("Summer", "Summer")],
                default="Spring",
                max_length=6,
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="course",
            name="term_year",
            field=models.CharField(default="2023", max_length=4),
            preserve_default=False,
        ),
    ]
