# Generated by Django 4.1.7 on 2023-04-26 02:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("TAScheduler", "0004_course_number"),
    ]

    operations = [
        migrations.AlterField(
            model_name="section",
            name="course",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="sections",
                to="TAScheduler.course",
            ),
        ),
    ]