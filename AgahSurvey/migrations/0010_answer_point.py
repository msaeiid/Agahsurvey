# Generated by Django 3.2.4 on 2021-07-22 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AgahSurvey', '0009_alter_answer_option'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='point',
            field=models.PositiveSmallIntegerField( editable=False, verbose_name='امتیاز'),
            preserve_default=False,
        ),
    ]
