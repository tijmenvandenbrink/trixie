from rest_framework import serializers
from apps.organizations.models import Organization
from apps.services.models import Service
from apps.devices.models import Device


class OrganizationSerializer(serializers.HyperlinkedModelSerializer):
    services = serializers.HyperlinkedRelatedField(many=True, queryset=Service.objects.all(),  view_name='service-detail')
    devices = serializers.HyperlinkedRelatedField(many=True, queryset=Device.objects.all(), view_name='device-detail')

    class Meta:
        model = Organization
        fields = ('url', 'name', 'abbreviation', 'services', 'devices')