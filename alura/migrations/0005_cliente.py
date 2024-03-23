# Generated by Django 5.0.3 on 2024-03-21 21:56

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alura', '0004_alter_curso_sku'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('dni', models.CharField(max_length=8)),
                ('sexo', models.CharField(max_length=1)),
                ('telefono', models.CharField(max_length=20)),
                ('fecha_nacimiento', models.DateField(null=True)),
                ('direccion', models.TextField()),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'tbl_cliente',
            },
        ),
    ]
