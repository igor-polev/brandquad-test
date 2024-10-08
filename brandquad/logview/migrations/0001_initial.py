# Generated by Django 5.1.1 on 2024-09-27 15:59

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Log",
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
                ("time", models.DateTimeField()),
                ("remote_ip", models.CharField(max_length=15)),
                ("remote_user", models.CharField(max_length=64)),
                ("request", models.CharField(max_length=2048)),
                ("response", models.IntegerField()),
                ("bytes", models.IntegerField()),
                ("referrer", models.CharField(max_length=64)),
                ("agent", models.CharField(max_length=512)),
                ("method", models.CharField(max_length=8)),
                ("request_uri", models.CharField(max_length=2048)),
            ],
        ),
    ]
