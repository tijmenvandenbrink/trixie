from django.contrib import admin
from apps.organizations.models import Organization


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'abbreviation')
    search_fields = ('name', 'abbreviation')
    list_display_links = ('name',)


admin.site.register(Organization, OrganizationAdmin)