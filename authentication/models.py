from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import Group

class User(AbstractUser):
    CREATOR = 'CREATOR'
    SUBSCRIBER = 'SUBSCRIBER'

    ROLE_CHOICES = (
        (CREATOR, 'Créateur'),
        (SUBSCRIBER, 'Abonné'),
    )
    profile_photo = models.ImageField(verbose_name='photo de profil')
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, verbose_name='rôle')
    follows = models.ManyToManyField(
        'self',
        limit_choices_to={'role': CREATOR},
        symmetrical=False,
        verbose_name='suit',
    )
    
    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)

        if is_new:
            if self.role == 'CREATOR':
                group = Group.objects.get(name='creators')
                self.groups.add(group)
            elif self.role == 'SUBSCRIBER':
                group = Group.objects.get(name='subscribers')
                self.groups.add(group)
