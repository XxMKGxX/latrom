from django.conf.urls import url
from services import views
from rest_framework import routers

service_router = routers.DefaultRouter()
service_router.register('api/service', views.ServiceAPIView)

service_urls = [
    url(r'^create-service$', views.ServiceCreateView.as_view(), name='create-service'),
    url(r'^list-services$', views.ServiceListView.as_view(), name='list-services'),
    url(r'^service-update/(?P<pk>[\d]+)/$', views.ServiceUpdateView.as_view(), name='service-update'),
    url(r'^service-detail/(?P<pk>[\d]+)/?$', views.ServiceDetailView.as_view(), name='service-details'),
] + service_router.urls 
