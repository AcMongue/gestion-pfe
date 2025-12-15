# Generated migration to add DefenseJury model and deprecate JuryMember

from django.db import migrations, models
import django.core.validators
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('defenses', '0001_initial'),  # Ajustez selon votre dernière migration
        ('users', '0005_rename_supervisor_to_teacher'),
    ]

    operations = [
        migrations.CreateModel(
            name='DefenseJury',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('president', 'Président'), ('examiner', 'Examinateur'), ('rapporteur', 'Rapporteur')], max_length=20, verbose_name='Rôle dans le jury')),
                ('grade', models.DecimalField(blank=True, decimal_places=2, help_text='Note attribuée par ce membre du jury', max_digits=4, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(20)], verbose_name='Note sur 20')),
                ('comments', models.TextField(blank=True, help_text='Observations et commentaires sur le projet', verbose_name='Commentaires')),
                ('graded_at', models.DateTimeField(blank=True, null=True, verbose_name='Date de notation')),
                ('defense', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='defense_jury_members', to='defenses.defense', verbose_name='Soutenance')),
                ('teacher', models.ForeignKey(limit_choices_to={'role': 'teacher'}, on_delete=django.db.models.deletion.CASCADE, to='users.user', verbose_name='Enseignant')),
            ],
            options={
                'verbose_name': 'Membre du jury',
                'verbose_name_plural': 'Membres du jury',
                'ordering': ['role', 'teacher'],
                'unique_together': {('defense', 'teacher')},
            },
        ),
    ]
