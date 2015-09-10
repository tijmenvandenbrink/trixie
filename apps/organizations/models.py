from django.db import models

from taggit.managers import TaggableManager


class Organization(models.Model):
    name = models.CharField(max_length=75)
    abbreviation = models.CharField(max_length=25)
    tags = TaggableManager(blank=True)

    def __unicode__(self):
        return "%s" % self.name