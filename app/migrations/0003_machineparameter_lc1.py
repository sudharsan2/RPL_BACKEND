# Generated by Django 5.0.6 on 2024-08-24 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_breakdowndetail_workorderheader_breakdowndetail'),
    ]

    operations = [
        migrations.AddField(
            model_name='machineparameter',
            name='lc1',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
