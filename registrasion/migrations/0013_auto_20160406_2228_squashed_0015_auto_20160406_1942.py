# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-04-07 03:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    replaces = [('registrasion', '0013_auto_20160406_2228'), ('registrasion', '0014_auto_20160406_1847'), ('registrasion', '0015_auto_20160406_1942')]

    dependencies = [
        ('registrasion', '0012_auto_20160406_1212'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentBase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(default=django.utils.timezone.now)),
                ('reference', models.CharField(max_length=255)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=8)),
            ],
        ),
        migrations.RemoveField(
            model_name='payment',
            name='invoice',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='paid',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='void',
        ),
        migrations.AddField(
            model_name='invoice',
            name='due_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='invoice',
            name='issue_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='invoice',
            name='recipient',
            field=models.CharField(default='Lol', max_length=1024),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='invoice',
            name='status',
            field=models.IntegerField(choices=[(1, 'Unpaid'), (2, 'Paid'), (3, 'Refunded'), (4, 'VOID')], db_index=True),
        ),
        migrations.AddField(
            model_name='lineitem',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='registrasion.Product'),
        ),
        migrations.CreateModel(
            name='ManualPayment',
            fields=[
                ('paymentbase_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='registrasion.PaymentBase')),
            ],
            bases=('registrasion.paymentbase',),
        ),
        migrations.DeleteModel(
            name='Payment',
        ),
        migrations.AddField(
            model_name='paymentbase',
            name='invoice',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='registrasion.Invoice'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='cart_revision',
            field=models.IntegerField(db_index=True, null=True),
        ),
    ]