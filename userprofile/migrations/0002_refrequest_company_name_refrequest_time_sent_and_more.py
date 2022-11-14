# Generated by Django 4.1.2 on 2022-11-13 21:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("userprofile", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="refrequest",
            name="company_name",
            field=models.CharField(
                blank=True, max_length=100, null=True, verbose_name="company name"
            ),
        ),
        migrations.AddField(
            model_name="refrequest",
            name="time_sent",
            field=models.DateTimeField(
                auto_now_add=True, null=True, verbose_name="time_sent"
            ),
        ),
        migrations.AlterField(
            model_name="refrequest",
            name="status",
            field=models.CharField(
                choices=[
                    ("UNIN", "Uninitiated"),
                    ("PEND", "Pending"),
                    ("COMP", "Complete"),
                ],
                default="UNIN",
                max_length=4,
                verbose_name="status",
            ),
        ),
        migrations.AlterField(
            model_name="refrequest",
            name="to_email",
            field=models.EmailField(
                blank=True, max_length=254, null=True, verbose_name="to email"
            ),
        ),
        migrations.CreateModel(
            name="RefResponse",
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
                ("email", models.EmailField(max_length=254, verbose_name="email")),
                (
                    "first_name",
                    models.CharField(
                        blank=True, max_length=50, null=True, verbose_name="first name"
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True, max_length=50, null=True, verbose_name="last name"
                    ),
                ),
                (
                    "company_name",
                    models.CharField(
                        blank=True,
                        max_length=50,
                        null=True,
                        verbose_name="company name",
                    ),
                ),
                ("title", models.CharField(max_length=50, verbose_name="title")),
                (
                    "relation",
                    models.CharField(
                        choices=[
                            ("BOSS", "Boss to referee"),
                            ("COLL", "Colleague to referee"),
                            ("CONS", "referee was consultant"),
                            ("OTH", "Other"),
                        ],
                        default="BOSS",
                        max_length=4,
                        verbose_name="relation to referee",
                    ),
                ),
                (
                    "other_relation",
                    models.CharField(
                        max_length=80, verbose_name="if Other, please specify"
                    ),
                ),
                ("main_tasks", models.TextField(verbose_name="describe main tasks")),
                ("elaborate", models.TextField(verbose_name="elaborate")),
                ("extra", models.TextField(verbose_name="extra")),
                (
                    "referee_first_name",
                    models.CharField(max_length=50, verbose_name="referee first name"),
                ),
                (
                    "referee_last_name",
                    models.CharField(max_length=50, verbose_name="referee last name"),
                ),
                (
                    "time_added",
                    models.DateTimeField(auto_now=True, verbose_name="time added"),
                ),
                (
                    "ref_request",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="userprofile.refrequest",
                        verbose_name="ref request",
                    ),
                ),
            ],
            options={
                "verbose_name": "Reference response",
                "verbose_name_plural": "Reference requests",
            },
        ),
    ]
