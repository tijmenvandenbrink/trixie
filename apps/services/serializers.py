from rest_framework import serializers
from apps.services.models import Service, ServiceStatus, ServiceType
from apps.organizations.models import Organization
from apps.devices.models import Device
from apps.components.models import Component


class ServiceTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ServiceType
        fields = ('url', 'name')


class ServiceStatusSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ServiceStatus
        fields = ('url', 'name', 'conversion')


class ServiceSerializer(serializers.HyperlinkedModelSerializer):
    status = serializers.HyperlinkedRelatedField(queryset=ServiceStatus.objects.all(), view_name='servicestatus-detail')
    service_type = serializers.HyperlinkedRelatedField(queryset=ServiceType.objects.all(), view_name='servicetype-detail')
    organization = serializers.HyperlinkedRelatedField(many=True, queryset=Organization.objects.all(),
                                                       view_name='organization-detail')
    device = serializers.HyperlinkedRelatedField(many=True, queryset=Device.objects.all(), view_name='device-detail')
    component = serializers.HyperlinkedRelatedField(many=True, queryset=Component.objects.all(), view_name='component-detail')
    sub_services = serializers.HyperlinkedRelatedField(many=True, queryset=Service.objects.all(), view_name='service-detail')

    class Meta:
        model = Service
        fields = ('url', 'name', 'description', 'status', 'service_type', 'organization', 'device', 'component',
                  'frequency', 'start', 'end', 'service_window', 'sub_services')