# Generated by Django 4.2 on 2024-07-24 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("sl500_dd", "0002_alter_sl500p_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="sl500",
            name="id",
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
    ]