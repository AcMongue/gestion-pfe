from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta, date
from django.utils import timezone
from users.models import User
from projects.models import Project


class Room(models.Model):
    """Modèle représentant une salle de soutenance."""
    
    # Liste complète des salles disponibles
    ROOM_CHOICES = [
        # Salles côté BS (Bloc des Spécialités)
        ('17BS1', 'Salle 17BS1'),
        ('16BS1', 'Salle 16BS1'),
        ('15BS1', 'Salle 15BS1'),
        ('14BS1', 'Salle 14BS1'),
        ('13BS1', 'Salle 13BS1'),
        ('12BS1', 'Salle 12BS1'),
        ('10BS1', 'Salle 10BS1'),
        ('30BS2', 'Salle 30BS2'),
        ('31BS2', 'Salle 31BS2'),
        ('32BS2', 'Salle 32BS2'),
        ('33BS2', 'Salle 33BS2'),
        ('34BS2', 'Salle 34BS2'),
        ('29BS2', 'Salle 29BS2'),
        ('27BS2', 'Salle 27BS2'),
        ('26BS2', 'Salle 26BS2'),
        ('24BS2', 'Salle 24BS2'),
        ('25BS2', 'Salle 25BS2'),
        ('23BS2', 'Salle 23BS2'),
        ('22BS2', 'Salle 22BS2'),
        ('21BS2', 'Salle 21BS2'),
        ('20BS2', 'Salle 20BS2'),
        ('19BS2', 'Salle 19BS2'),
        ('18BS2', 'Salle 18BS2'),
        # Salles côté BP (Bloc Pédagogique)
        ('17BP1', 'Salle 17BP1'),
        ('16BP1', 'Salle 16BP1'),
        ('15BP1', 'Salle 15BP1'),
        ('14BP1', 'Salle 14BP1'),
        ('13BP1', 'Salle 13BP1'),
        ('12BP1', 'Salle 12BP1'),
        ('10BP1', 'Salle 10BP1'),
        ('30BP2', 'Salle 30BP2'),
        ('31BP2', 'Salle 31BP2'),
        ('32BP2', 'Salle 32BP2'),
        ('33BP2', 'Salle 33BP2'),
        ('34BP2', 'Salle 34BP2'),
        ('29BP2', 'Salle 29BP2'),
        ('27BP2', 'Salle 27BP2'),
        ('26BP2', 'Salle 26BP2'),
        ('24BP2', 'Salle 24BP2'),
        ('25BP2', 'Salle 25BP2'),
        ('23BP2', 'Salle 23BP2'),
        ('22BP2', 'Salle 22BP2'),
        ('21BP2', 'Salle 21BP2'),
        ('20BP2', 'Salle 20BP2'),
        ('19BP2', 'Salle 19BP2'),
        ('18BP2', 'Salle 18BP2'),
    ]
    
    # Filières (mêmes que User.FILIERE_CHOICES)
    FILIERE_CHOICES = [
        ('GIT', 'Génie Informatique & Télécommunications'),
        ('GESI', 'Génie Électrique et Systèmes Intelligents'),
        ('GQHSEI', 'Génie de la Qualité Hygiène, Sécurité et Environnement Industriel'),
        ('GAM', 'Génie Automobile et Mécatronique'),
        ('GMP', 'Génie Maritime et Portuaire'),
        ('GP', 'Génie des Procédés'),
        ('GE', 'Génie Énergétique'),
        ('GM', 'Génie Mécanique'),
        ('GC', 'Génie Civil'),
        ('GENERAL', 'Usage Général'),  # Pour salles partagées
    ]
    
    # Nom de la salle (sélection dans la liste prédéfinie)
    name = models.CharField(
        _('nom de la salle'),
        max_length=10,
        choices=ROOM_CHOICES,
        unique=True,
        help_text='Sélectionnez une salle dans la liste'
    )
    
    filiere = models.CharField(
        _('filière'),
        max_length=10,
        choices=FILIERE_CHOICES,
        default='GENERAL',
        help_text='Filière prioritaire pour cette salle'
    )
    
    capacity = models.PositiveIntegerField(
        _('capacité'),
        help_text='Nombre de places assises'
    )
    
    equipment = models.TextField(
        _('équipement disponible'),
        blank=True,
        help_text='Ex: Projecteur, tableau blanc, son'
    )
    
    is_available = models.BooleanField(
        _('disponible'),
        default=True
    )
    
    @property
    def building(self):
        """Extrait le bâtiment du nom de la salle (BP ou BS)."""
        if 'BP' in self.name:
            return 'BP'
        elif 'BS' in self.name:
            return 'BS'
        return ''
    
    @property
    def floor(self):
        """Extrait l'étage du nom de la salle (1 ou 2)."""
        if self.name:
            return self.name[-1]
        return ''
    
    @property
    def room_number(self):
        """Extrait le numéro de la salle."""
        if self.name and len(self.name) >= 4:
            return self.name[:2]
        return ''
    
    @property
    def nomenclature(self):
        """Retourne la nomenclature complète (ex: 15BS1)."""
        return self.name
    
    class Meta:
        verbose_name = _('salle')
        verbose_name_plural = _('salles')
        ordering = ['name']
    
    def __str__(self):
        filiere_display = self.get_filiere_display() if self.filiere != 'GENERAL' else ''
        if filiere_display:
            return f"{self.name} - {filiere_display}"
        return self.name
    
    def save(self, *args, **kwargs):
        """Validation avant sauvegarde."""
        super().save(*args, **kwargs)
        return self.name
    
    def clean(self):
        """Validation personnalisée"""
        super().clean()
        
        # Le nom est maintenant sélectionné dans ROOM_CHOICES
        # Pas besoin de validation supplémentaire
        pass
    
    def save(self, *args, **kwargs):
        """Sauvegarder la salle"""
        # Le nom est déjà défini via le formulaire (choix dans ROOM_CHOICES)
        # Pas besoin de génération automatique
        super().save(*args, **kwargs)
    
    def is_available_for_defense(self, defense_date, defense_time, duration):
        """Vérifie si la salle est disponible pour une soutenance."""
        if not self.is_available:
            return False
        
        from datetime import datetime, timedelta
        end_time = (datetime.combine(defense_date, defense_time) + timedelta(minutes=duration)).time()
        
        # Vérifier les conflits
        conflicts = Defense.objects.filter(
            room_obj=self,
            date=defense_date,
            status='scheduled'
        )
        
        for conflict in conflicts:
            conflict_end = conflict.get_end_time()
            if not (defense_time >= conflict_end or end_time <= conflict.time):
                return False
        
        return True


class Defense(models.Model):
    """Modèle représentant une soutenance de PFE avec détection de conflits."""
    
    STATUS_CHOICES = [
        ('scheduled', 'Planifiée'),
        ('in_progress', 'En cours'),
        ('completed', 'Terminée'),
        ('cancelled', 'Annulée'),
        ('rescheduled', 'Reportée'),
    ]
    
    project = models.OneToOneField(
        Project,
        on_delete=models.CASCADE,
        related_name='defense',
        verbose_name=_('projet')
    )
    
    date = models.DateField(_('date'))
    time = models.TimeField(_('heure'))
    duration = models.PositiveIntegerField(_('durée (minutes)'), default=30)
    
    room_obj = models.ForeignKey(
        Room,
        on_delete=models.SET_NULL,
        related_name='defenses',
        verbose_name=_('salle'),
        null=True,
        blank=True
    )
    
    # Ancien champ room conservé pour compatibilité
    room = models.CharField(_('salle (ancien)'), max_length=100, blank=True)
    building = models.CharField(_('bâtiment (ancien)'), max_length=100, blank=True)
    
    status = models.CharField(
        _('statut'),
        max_length=20,
        choices=STATUS_CHOICES,
        default='scheduled'
    )
    
    presentation_duration = models.PositiveIntegerField(
        _('durée présentation (min)'),
        default=15
    )
    
    questions_duration = models.PositiveIntegerField(
        _('durée questions (min)'),
        default=15
    )
    
    final_grade = models.DecimalField(
        _('note finale'),
        max_digits=4,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(20)]
    )
    
    jury_comments = models.TextField(_('commentaires du jury'), blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('soutenance')
        verbose_name_plural = _('soutenances')
        ordering = ['date', 'time']
    
    def __str__(self):
        return f"{self.project.title} - {self.date} {self.time}"
    
    def get_end_time(self):
        """Calcule l'heure de fin de la soutenance."""
        start = datetime.combine(self.date, self.time)
        end = start + timedelta(minutes=self.duration)
        return end.time()
    
    def check_room_conflict(self):
        """Vérifie les conflits de salle."""
        if not self.room_obj:
            return []
        
        end_time = self.get_end_time()
        conflicts = Defense.objects.filter(
            room_obj=self.room_obj,
            date=self.date,
            status='scheduled'
        ).exclude(pk=self.pk)
        
        conflicting = []
        for other in conflicts:
            other_end = other.get_end_time()
            # Vérifier chevauchement des horaires
            if not (self.time >= other_end or end_time <= other.time):
                conflicting.append(other)
        
        return conflicting
    
    def check_jury_conflicts(self):
        """Vérifie les conflits de jury (mêmes personnes, même horaire)."""
        jury_members = self.jury_members.all().values_list('user', flat=True)
        if not jury_members:
            return []
        
        end_time = self.get_end_time()
        other_defenses = Defense.objects.filter(
            date=self.date,
            status='scheduled'
        ).exclude(pk=self.pk)
        
        conflicts = []
        for other in other_defenses:
            other_end = other.get_end_time()
            # Vérifier chevauchement des horaires
            if not (self.time >= other_end or end_time <= other.time):
                # Vérifier si des membres du jury sont communs
                other_jury = other.jury_members.all().values_list('user', flat=True)
                common_members = set(jury_members) & set(other_jury)
                if common_members:
                    conflicts.append({
                        'defense': other,
                        'common_members': list(common_members)
                    })
        
        return conflicts
    
    def get_president(self):
        """Retourne le président du jury."""
        return self.jury_members.filter(role='president').first()
    
    def calculate_final_grade(self):
        """
        Calcule la note finale comme moyenne simple des notes du jury.
        Retourne None si toutes les notes ne sont pas saisies.
        """
        jury_members = self.jury_members.all()
        
        if not jury_members.exists():
            return None
        
        # Vérifier que tous les membres ont noté
        grades = [member.grade for member in jury_members if member.grade is not None]
        
        if len(grades) != jury_members.count():
            return None  # Toutes les notes pas encore saisies
        
        # Moyenne simple
        avg_grade = sum(grades) / len(grades)
        self.final_grade = round(avg_grade, 2)
        return self.final_grade
    
    def validate_jury_composition(self):
        """
        Valide la composition du jury selon les règles:
        - Standard: 1 président, 2 examinateurs, 1 rapporteur
        - Interdisciplinaire: 1 président, 2+ examinateurs, 2 rapporteurs
        
        Returns:
            tuple: (is_valid, errors_list)
        """
        jury_members = self.jury_members.all()
        errors = []
        
        # Compter par rôle
        president_count = jury_members.filter(role='president').count()
        examiner_count = jury_members.filter(role='examiner').count()
        rapporteur_count = jury_members.filter(role='rapporteur').count()
        
        # Vérification président (toujours 1)
        if president_count == 0:
            errors.append("Un président est requis.")
        elif president_count > 1:
            errors.append("Un seul président est autorisé.")
        
        # Vérifier si projet interdisciplinaire
        is_interdisciplinary = self.project.assignment.subject.is_interdisciplinary
        
        if is_interdisciplinary:
            # Jury élargi: 2+ examinateurs, 2 rapporteurs
            if examiner_count < 2:
                errors.append("Un projet interdisciplinaire nécessite au moins 2 examinateurs.")
            if rapporteur_count < 2:
                errors.append("Un projet interdisciplinaire nécessite 2 rapporteurs (les encadreurs).")
        else:
            # Jury standard: 2 examinateurs, 1 rapporteur
            if examiner_count < 2:
                errors.append("Au moins 2 examinateurs sont requis.")
            if rapporteur_count != 1:
                errors.append("Exactement 1 rapporteur est requis (l'encadreur principal).")
        
        return (len(errors) == 0, errors)
    
    @property
    def is_fully_graded(self):
        """Vérifie si tous les membres du jury ont noté."""
        return self.calculate_final_grade() is not None
    
    @property
    def can_be_graded(self):
        """Vérifie si la soutenance peut être notée (date passée)."""
        defense_datetime = datetime.combine(self.date, self.time)
        return defense_datetime <= datetime.now()
    
    def clean(self):
        """Validation avec détection de conflits."""
        super().clean()
        
        # Vérifier conflits de salle
        room_conflicts = self.check_room_conflict()
        if room_conflicts:
            raise ValidationError(
                f"Conflit de salle avec {len(room_conflicts)} autre(s) soutenance(s)"
            )
        
        # Vérifier conflits de jury
        jury_conflicts = self.check_jury_conflicts()
        if jury_conflicts:
            raise ValidationError(
                f"Conflit de jury avec {len(jury_conflicts)} autre(s) soutenance(s)"
            )


class JuryMember(models.Model):
    """Modèle représentant un membre du jury pour une soutenance avec validation des rôles."""
    
    ROLE_CHOICES = [
        ('president', 'Président'),
        ('examiner', 'Examinateur'),
        ('supervisor', 'Encadreur'),
        ('guest', 'Invité'),
    ]
    
    defense = models.ForeignKey(
        Defense,
        on_delete=models.CASCADE,
        related_name='jury_members',
        verbose_name=_('soutenance')
    )
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='jury_assignments',
        verbose_name=_('membre')
    )
    
    role = models.CharField(
        _('rôle'),
        max_length=20,
        choices=ROLE_CHOICES
    )
    
    is_president = models.BooleanField(
        _('est président'),
        default=False,
        help_text='Seuls les Professeurs peuvent être présidents'
    )
    
    grade = models.DecimalField(
        _('note'),
        max_digits=4,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(20)]
    )
    
    comments = models.TextField(_('commentaires'), blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _('membre du jury')
        verbose_name_plural = _('membres du jury')
        unique_together = ['defense', 'user']
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.get_role_display()}"
    
    def clean(self):
        """Validation des règles de jury."""
        super().clean()
        
        # Vérifier que seul un Professeur peut être président
        if self.is_president or self.role == 'president':
            if not self.user.can_be_jury_president:
                raise ValidationError(
                    "Seuls les Professeurs peuvent être présidents de jury"
                )
            
            # Vérifier la limite de 4 soutenances comme président
            president_count = JuryMember.objects.filter(
                user=self.user,
                is_president=True,
                defense__date=self.defense.date,
                defense__status='scheduled'
            ).exclude(pk=self.pk).count()
            
            if president_count >= 4:
                raise ValidationError(
                    f"{self.user.get_full_name()} a déjà 4 soutenances comme président ce jour-là"
                )
    
    def save(self, *args, **kwargs):
        # Synchroniser is_president avec role
        if self.role == 'president':
            self.is_president = True
        super().save(*args, **kwargs)


class DefenseEvaluation(models.Model):
    """Modèle représentant l'évaluation détaillée d'une soutenance."""
    
    defense = models.OneToOneField(Defense, on_delete=models.CASCADE, related_name='evaluation', verbose_name=_('soutenance'))
    presentation_quality = models.PositiveIntegerField(_('qualité présentation'), validators=[MinValueValidator(0), MaxValueValidator(20)], null=True, blank=True)
    content_mastery = models.PositiveIntegerField(_('maîtrise du contenu'), validators=[MinValueValidator(0), MaxValueValidator(20)], null=True, blank=True)
    technical_skills = models.PositiveIntegerField(_('compétences techniques'), validators=[MinValueValidator(0), MaxValueValidator(20)], null=True, blank=True)
    communication = models.PositiveIntegerField(_('communication'), validators=[MinValueValidator(0), MaxValueValidator(20)], null=True, blank=True)
    answers_quality = models.PositiveIntegerField(_('qualité des réponses'), validators=[MinValueValidator(0), MaxValueValidator(20)], null=True, blank=True)
    overall_impression = models.TextField(_('impression générale'), blank=True)
    strengths = models.TextField(_('points forts'), blank=True)
    weaknesses = models.TextField(_('points à améliorer'), blank=True)
    recommendations = models.TextField(_('recommandations'), blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('évaluation de soutenance')
        verbose_name_plural = _('évaluations de soutenance')
    
    def __str__(self):
        return f"Évaluation - {self.defense.project.title}"


class DefenseChangeRequest(models.Model):
    """Modèle pour les demandes de modification de soutenance."""
    
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('approved', 'Approuvée'),
        ('rejected', 'Rejetée'),
    ]
    
    defense = models.ForeignKey(
        Defense,
        on_delete=models.CASCADE,
        related_name='change_requests',
        verbose_name=_('soutenance')
    )
    requested_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='defense_change_requests',
        verbose_name=_('demandé par')
    )
    proposed_date = models.DateField(_('date proposée'), null=True, blank=True)
    proposed_time = models.TimeField(_('heure proposée'), null=True, blank=True)
    proposed_location = models.CharField(_('lieu proposé'), max_length=200, blank=True)
    reason = models.TextField(_('motif'))
    status = models.CharField(
        _('statut'),
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    reviewed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='reviewed_defense_changes',
        verbose_name=_('examiné par'),
        null=True,
        blank=True
    )
    review_comment = models.TextField(_('commentaire de révision'), blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(_('examiné le'), null=True, blank=True)
    
    class Meta:
        verbose_name = _('demande de modification de soutenance')
        verbose_name_plural = _('demandes de modification de soutenance')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Demande de {self.requested_by.get_full_name()} - {self.get_status_display()}"


class DefenseJury(models.Model):
    """
    Modèle représentant un membre du jury d'une soutenance.
    Les membres du jury sont des enseignants (role='teacher') avec différents rôles.
    """
    
    ROLE_CHOICES = [
        ('president', 'Président'),
        ('examiner', 'Examinateur'),
        ('rapporteur', 'Rapporteur'),
    ]
    
    defense = models.ForeignKey(
        Defense, 
        on_delete=models.CASCADE, 
        related_name='defense_jury_members',
        verbose_name='Soutenance'
    )
    
    teacher = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'teacher'},
        verbose_name='Enseignant'
    )
    
    role = models.CharField(
        max_length=20, 
        choices=ROLE_CHOICES,
        verbose_name='Rôle dans le jury'
    )
    
    grade = models.DecimalField(
        max_digits=4, 
        decimal_places=2,
        null=True, 
        blank=True,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(20)
        ],
        verbose_name='Note sur 20',
        help_text='Note attribuée par ce membre du jury'
    )
    
    comments = models.TextField(
        blank=True,
        verbose_name='Commentaires',
        help_text='Observations et commentaires sur le projet'
    )
    
    graded_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Date de notation'
    )
    
    class Meta:
        verbose_name = 'Membre du jury'
        verbose_name_plural = 'Membres du jury'
        unique_together = ['defense', 'teacher']
        ordering = ['role', 'teacher']
    
    def __str__(self):
        return f"{self.teacher.get_full_name()} - {self.get_role_display()}"
    
    def clean(self):
        """Validation des contraintes sur les membres du jury."""
        super().clean()
        
        # 1. Vérifier que l'enseignant a le rôle 'teacher'
        if self.teacher.role != 'teacher':
            raise ValidationError({
                'teacher': "Seuls les enseignants peuvent être membres d'un jury."
            })
        
        # 2. Seuls les Professeurs peuvent être présidents
        if self.role == 'president' and self.teacher.academic_title != 'professeur':
            raise ValidationError({
                'role': "Seul un Professeur peut être président de jury. "
                        f"{self.teacher.get_full_name()} est {self.teacher.get_academic_title_display()}."
            })
        
        # 3. Vérifier la limite de 4 présidences par jour et par département
        if self.role == 'president' and self.defense.date:
            defense_date = self.defense.date
            department = self.defense.project.assignment.subject.filiere
            
            presidencies_today = DefenseJury.objects.filter(
                teacher=self.teacher,
                role='president',
                defense__date=defense_date,
                defense__project__assignment__subject__filiere=department
            ).exclude(pk=self.pk).count()
            
            if presidencies_today >= 4:
                raise ValidationError({
                    'teacher': f"Le professeur {self.teacher.get_full_name()} a déjà 4 présidences "
                               f"prévues ce jour dans le département {department}."
                })
        
        # 4. Un enseignant ne peut avoir qu'un seul rôle dans une soutenance
        if self.pk is None:  # Nouvelle instance uniquement
            existing = DefenseJury.objects.filter(
                defense=self.defense,
                teacher=self.teacher
            ).exists()
            
            if existing:
                raise ValidationError({
                    'teacher': f"{self.teacher.get_full_name()} est déjà membre de ce jury."
                })
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    @property
    def can_grade(self):
        """Vérifie si ce membre peut noter (soutenance passée)."""
        if not self.defense.date:
            return False
        defense_datetime = datetime.combine(self.defense.date, self.defense.time)
        return defense_datetime <= datetime.now()
