# Generated by Django 4.2 on 2024-07-24 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("sl500_dd", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="sl500p",
            name="id",
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
    ]
