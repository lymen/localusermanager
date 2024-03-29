# Generated by Django 3.1.1 on 2020-09-27 16:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=120, unique=True)),
                ('password', models.CharField(max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name='SuperAdmin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=120, unique=True)),
                ('password', models.CharField(max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name='UserGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('groupname', models.CharField(max_length=120, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=120, unique=True)),
                ('password', models.CharField(max_length=120)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='superadmin.usergroup')),
            ],
        ),
        migrations.CreateModel(
            name='AccountChangeLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=120)),
                ('modified', models.DateTimeField(auto_now_add=True)),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='superadmin.account')),
            ],
        ),
        migrations.AddField(
            model_name='account',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='superadmin.usergroup'),
        ),
    ]
