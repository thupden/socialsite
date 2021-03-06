# Generated by Django 3.0.8 on 2020-07-22 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userpage', '0002_auto_20200722_1203'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='userProfile',
            new_name='userImage',
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='connections',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='followers',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='following',
            field=models.IntegerField(default=0),
        ),
    ]
