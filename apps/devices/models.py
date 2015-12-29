from django.db import models

from taggit.managers import TaggableManager

from ..core.models import Timestamped
from ..organizations.models import Organization


class DeviceStatus(models.Model):
    name = models.CharField(max_length=50, unique=True)
    conversion = models.IntegerField()

    def __unicode__(self):
        return "{0} ({1})".format(self.name, self.conversion)

    class Meta:
        verbose_name_plural = 'Device statuses'


class Device(Timestamped):
    name = models.CharField(max_length=200)
    hostname = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=200, blank=True)
    device_type = models.CharField(max_length=200, blank=True)
    manufacturer = models.CharField(max_length=200, blank=True)
    serial = models.CharField(max_length=250, blank=True)
    location = models.TextField(blank=True)
    ip = models.GenericIPAddressField(blank=True, null=True)
    software_version = models.CharField(max_length=200, blank=True)
    status = models.ForeignKey(DeviceStatus)
    organization = models.ForeignKey(Organization, related_name='devices')
    tags = TaggableManager(blank=True)

    def __unicode__(self):
        return "{0}".format(self.name)