from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_init
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

    def __str__(self):
        return self.get_full_name()


@receiver(post_init, sender=User)
def user_post_init(sender, instance, **kwargs):
    """
    https://gist.github.com/troolee/1140516
    """
    def get_profile():
        user = instance
        if not hasattr(user, '_profile_cache'):
            user._profile_cache, _ = UserProfile._default_manager.using(user._state.db).get_or_create(user=user)
            user._profile_cache.user = user
        return user._profile_cache

    instance.get_profile = get_profile
