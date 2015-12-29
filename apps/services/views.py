from django.views.generic import ListView, DetailView

from rest_framework import viewsets, permissions, filters
from braces.views import OrderableListMixin, PrefetchRelatedMixin
from digg_paginator import DiggPaginator

from apps.services.serializers import ServiceSerializer, ServiceStatusSerializer, ServiceTypeSerializer
from apps.services.models import Service, ServiceStatus, ServiceType


class ServiceList(OrderableListMixin, PrefetchRelatedMixin, ListView):
    model = Service
    prefetch_related = [u"organization", u"status", u"service_type"]
    orderable_columns = (u"name", u"description",)
    orderable_columns_default = u"name"
    template_name = 'services.html'
    context_object_name = 'service_list'
    paginate_by = 20
    paginator_class = DiggPaginator


class ServiceDetail(DetailView):
    model = Service
    context_object_name = 'service'
    template_name = 'service_detail.html'

"""
    def get_context_data(self, **kwargs):
        context = super(ServiceDetail, self).get_context_data(**kwargs)
        datasources = DataSource.objects.filter(name__contains="Volume")
        context['data'] = create_multibarchart(self.get_object(), datasources)
        return context
"""

class ServiceViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    """
    queryset = Service.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = ServiceSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('name', 'device', 'component', 'service_type', 'status', 'service_window')


class ServiceStatusViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    """
    queryset = ServiceStatus.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = ServiceStatusSerializer


class ServiceTypeViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    """
    queryset = ServiceType.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = ServiceTypeSerializer