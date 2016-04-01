from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    avatar = models.CharField(max_length=255, blank=True)

    twitter = models.CharField(max_length=255, blank=True)
    slack = models.CharField(max_length=255, blank=True)

    def get_full_name(self):
        full_name = "%s %s" % (self.user.first_name, self.user.last_name)

        if not full_name.strip():
            display_name = self.user.username
        else:
            display_name = full_name

        return display_name.title()

    def get_short_name(self):
        full_name = "%s %s" % (self.user.first_name, self.user.last_name[0] + '.' if self.user.last_name else '')

        if not full_name.strip():
            display_name = self.user.username
        else:
            display_name = full_name

        return display_name.title()

    def __str__(self):
        return self.get_full_name()


@receiver(post_save, sender=User)
def create_profile(sender, **kwargs):
    UserProfile.objects.get_or_create(user=kwargs['instance'])
