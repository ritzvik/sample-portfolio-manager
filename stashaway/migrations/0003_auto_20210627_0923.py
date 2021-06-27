# Generated by Django 3.1 on 2021-06-27 09:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("stashaway", "0002_deposit_amount"),
    ]

    operations = [
        migrations.AddField(
            model_name="deposit",
            name="deposit_type",
            field=models.CharField(
                choices=[("LUMPSUM", "LUMPSUM"), ("RECURRING", "RECURRING")],
                default="LUMPSUM",
                max_length=100,
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="monthlyrecurringdepositschedule",
            name="portfolio",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="stashaway.portfolio",
                unique=True,
            ),
        ),
    ]
