# Generated by Django 3.2.6 on 2021-12-20 02:55

import datetime
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0003_auto_20211215_1920'),
    ]

    operations = [
        migrations.CreateModel(
            name='Class',
            fields=[
                ('classid', models.CharField(max_length=20, primary_key=True, serialize=False, verbose_name='ClassId')),
                ('classname', models.CharField(max_length=100, verbose_name='Classname')),
                ('semester', models.CharField(max_length=20, verbose_name='Semester')),
                ('grade', models.CharField(max_length=20, verbose_name='Grade')),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('teacherid', models.CharField(max_length=20, primary_key=True, serialize=False, verbose_name='TeacherId')),
                ('teacher_name', models.CharField(max_length=20, verbose_name='TeacherName')),
                ('passward', models.CharField(max_length=20, verbose_name='passward')),
            ],
        ),
        migrations.AlterField(
            model_name='borrowrecord',
            name='end_day',
            field=models.DateTimeField(default=datetime.datetime(2021, 12, 27, 2, 55, 34, 537968, tzinfo=utc)),
        ),
        migrations.CreateModel(
            name='Reference_Book',
            fields=[
                ('ISBN', models.CharField(max_length=100, primary_key=True, serialize=False, verbose_name='ISBN')),
                ('bookname', models.CharField(max_length=100, verbose_name='BookName')),
                ('author', models.CharField(max_length=100, verbose_name='Author')),
                ('publisher', models.CharField(max_length=100, verbose_name='Publisher')),
                ('pub_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='pub_date')),
                ('link', models.CharField(max_length=100, verbose_name='Link')),
                ('type', models.CharField(max_length=20, verbose_name='Type')),
                ('class_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='book_class', to='book.class')),
            ],
        ),
        migrations.AddField(
            model_name='class',
            name='teacher',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='class_teacher', to='book.teacher'),
        ),
    ]