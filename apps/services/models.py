import logging

from django.db import models
from django.core.urlresolvers import reverse

from taggit.managers import TaggableManager

from ..core.models import Timestamped
from ..components.models import Component
from ..organizations.models import Organization
from ..devices.models import Device

logger = logging.getLogger(__name__)


class ServiceType(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __unicode__(self):
        return "{0}".format(self.name)


class ServiceStatus(models.Model):
    name = models.CharField(max_length=50, unique=True)
    conversion = models.IntegerField()

    def __unicode__(self):
        return "{0} ({1})".format(self.name, self.conversion)

    class Meta:
        verbose_name_plural = 'Service statuses'


SERVICE_WINDOW_CHOICES = (
    ('oh', 'Office Hours'),
    ('ooh', 'Out of Office Hours'),
    ('24x7', '24x7'),
)


class Service(Timestamped):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    organization = models.ManyToManyField(Organization, related_name='services')
    device = models.ManyToManyField(Device, null=True, blank=True, related_name='services')
    component = models.ManyToManyField(Component, null=True, blank=True, related_name='services')
    sub_services = models.ManyToManyField('self', null=True, blank=True, related_name='parent_service',
                                          symmetrical=False)
    service_type = models.ForeignKey(ServiceType)
    status = models.ForeignKey(ServiceStatus)
    start = models.DateField(null=True, blank=True)
    end = models.DateField(null=True, blank=True)
    frequency = models.PositiveIntegerField(blank=True)
    service_window = models.CharField(max_length=200, choices=SERVICE_WINDOW_CHOICES)
    tags = TaggableManager(blank=True)

    def __unicode__(self):
        return "{0}".format(self.id)

    def get_absolute_url(self):
        return reverse('apps.services.views.ServiceDetail', args=[str(self.id)])

    def get_datapoints(self, data_source, recursive=False):
        """ Returns a QuerySet of DataPoint objects of a given DataSource. With recursive=True all DataPoint
        objects of sub_services will also be returned.

        :param data_source: the DataSource for which to get the DataPoints
        :type data_source: DataSource object
        :param recursive: Include DataPoints from sub_services
        :type recursive: Boolean

        :returns: QuerySet
        """
        result = self.datapoint_set.filter(data_source=data_source)
        if recursive:
            # To eliminate the possibility of having loops we're recording the service_ids we already processed.
            path = set()
            path.add(self)
            if self.sub_services.all():
                for service in self.sub_services.all():
                    if service in path:
                        logger.warning('action="Detect service loop", status="LoopFound", component="service", '
                                       'result="Already got DataPoints for this service", service_name="{svc.name}", '
                                       'service_id="{svc.service_id}", service_type="{svc.service_type}", '
                                       'service_status="{svc.status}'.format(svc=service))
                        continue

                    path.add(service)
                    result = result | service.get_datapoints(data_source, recursive=True)

        return result