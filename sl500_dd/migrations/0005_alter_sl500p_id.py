# Generated by Django 4.2 on 2024-07-02 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("sl500_dd", "0004_alter_sl500_id_alter_sl500p_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="sl500p",
            name="id",
            field=models.BigIntegerField(primary_key=True, serialize=False),
        ),
    ]
