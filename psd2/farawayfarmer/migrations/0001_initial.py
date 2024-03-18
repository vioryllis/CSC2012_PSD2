# Generated by Django 4.2.11 on 2024-03-18 13:22

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Plant",
            fields=[
                ("plant_id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=100)),
                ("floor", models.CharField(max_length=50)),
                ("public", models.BooleanField(default=False)),
                (
                    "last_watered",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                (
                    "last_fertilized",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                ("auto_system", models.BooleanField(default=False)),
                (
                    "min_water_level",
                    models.DecimalField(decimal_places=2, max_digits=5),
                ),
                ("amt_to_water", models.DecimalField(decimal_places=2, max_digits=5)),
            ],
        ),
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                ("user_id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=100)),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("password", models.CharField(max_length=100)),
                ("floor", models.CharField(max_length=50)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="SensorData",
            fields=[
                ("sensor_data_id", models.AutoField(primary_key=True, serialize=False)),
                ("water_level", models.DecimalField(decimal_places=2, max_digits=5)),
                ("nutrient_level", models.DecimalField(decimal_places=2, max_digits=5)),
                (
                    "plant",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sensor_data",
                        to="farawayfarmer.plant",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="plant",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="plants",
                to="farawayfarmer.user",
            ),
        ),
    ]
