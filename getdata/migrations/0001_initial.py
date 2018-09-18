# Generated by Django 2.0.7 on 2018-09-14 20:17

from decimal import Decimal
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BatteryValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.DecimalField(decimal_places=5, max_digits=12, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='BatteryVariable',
            fields=[
                ('var_name', models.CharField(max_length=32, primary_key=True, serialize=False, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Day1Value',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=150, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Day1Variable',
            fields=[
                ('var_name', models.CharField(max_length=50, primary_key=True, serialize=False, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Genotype',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genotype', models.CharField(max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='ImagingValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.DecimalField(decimal_places=5, max_digits=12, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ImagingVariable',
            fields=[
                ('var_name', models.CharField(max_length=50, primary_key=True, serialize=False, unique=True)),
                ('vargroup', models.CharField(default='.', max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SNP',
            fields=[
                ('rs_id', models.CharField(max_length=32, primary_key=True, serialize=False, unique=True)),
                ('a1', models.CharField(default='.', max_length=2)),
                ('a2', models.CharField(default='.', max_length=2)),
                ('MAF', models.DecimalField(decimal_places=2, default=Decimal('-1.0'), max_digits=4)),
                ('chr_id', models.IntegerField(default=-1)),
                ('nchrobs', models.IntegerField(default=-1)),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('dns_id', models.CharField(max_length=10, primary_key=True, serialize=False, unique=True)),
                ('gender', models.CharField(default='.', max_length=2)),
                ('race_battery', models.CharField(default='.', max_length=2)),
                ('latino_battery', models.CharField(default='.', max_length=2)),
                ('age', models.IntegerField(default=-1)),
            ],
        ),
        migrations.AddField(
            model_name='snp',
            name='subjects',
            field=models.ManyToManyField(through='getdata.Genotype', to='getdata.Subject'),
        ),
        migrations.AddField(
            model_name='imagingvariable',
            name='subjects',
            field=models.ManyToManyField(through='getdata.ImagingValue', to='getdata.Subject'),
        ),
        migrations.AddField(
            model_name='imagingvalue',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='imgval', to='getdata.Subject'),
        ),
        migrations.AddField(
            model_name='imagingvalue',
            name='variable',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='getdata.ImagingVariable'),
        ),
        migrations.AddField(
            model_name='genotype',
            name='SNP',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='getdata.SNP'),
        ),
        migrations.AddField(
            model_name='genotype',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='genotype', to='getdata.Subject'),
        ),
        migrations.AddField(
            model_name='day1variable',
            name='subjects',
            field=models.ManyToManyField(through='getdata.Day1Value', to='getdata.Subject'),
        ),
        migrations.AddField(
            model_name='day1value',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='day1val', to='getdata.Subject'),
        ),
        migrations.AddField(
            model_name='day1value',
            name='variable',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='getdata.Day1Variable'),
        ),
        migrations.AddField(
            model_name='batteryvariable',
            name='subjects',
            field=models.ManyToManyField(through='getdata.BatteryValue', to='getdata.Subject'),
        ),
        migrations.AddField(
            model_name='batteryvalue',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='batval', to='getdata.Subject'),
        ),
        migrations.AddField(
            model_name='batteryvalue',
            name='variable',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='getdata.BatteryVariable'),
        ),
    ]
