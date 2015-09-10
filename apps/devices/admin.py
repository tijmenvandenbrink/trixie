from django.contrib import admin
from apps.devices.models import Device, DeviceStatus


class DeviceStatusAdmin(admin.ModelAdmin):
    list_display = ('name', 'conversion')


class DeviceAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'category', 'manufacturer', 'device_type', 'serial', 'location', 'ip',
                    'software_version', 'status')
    list_filter = ('category', 'manufacturer', 'device_type', 'software_version', 'status')
    search_fields = ('name', 'description', 'category', 'manufacturer', 'device_type', 'serial', 'location', 'ip',
                     'software_version', 'status')


admin.site.register(Device, DeviceAdmin)
admin.site.register(DeviceStatus, DeviceStatusAdmin)