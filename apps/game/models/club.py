from django.db import models
from django.conf import settings
from django.template.defaultfilters import slugify


class Club(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField(blank=True)
    logo = models.ImageField(blank=True, null=True)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='clubs', blank=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='my_clubs', default=1)

    #objects = ClubManager()

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super(Club, self).save(*args, **kwargs)

    def user_is_admin(self, user):
        return self.creator_id == user.id
