from rest_framework import serializers
from apps.devices.models import Device, DeviceStatus
from apps.organizations.models import Organization


class DeviceStatusSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DeviceStatus
        fields = ('url', 'name', 'conversion')


class DeviceSerializer(serializers.HyperlinkedModelSerializer):
    status = serializers.HyperlinkedRelatedField(queryset=DeviceStatus.objects.all(), view_name='devicestatus-detail')
    organization = serializers.HyperlinkedRelatedField(queryset=Organization.objects.all(), view_name='organization-detail')

    class Meta:
        model = Device
        fields = ('url', 'name', 'hostname', 'description', 'organization', 'category', 'manufacturer', 'device_type',
                  'serial', 'location', 'ip', 'software_version', 'status')