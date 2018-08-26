from django.conf.urls import url
from services import views
from rest_framework import routers


team_router = routers.DefaultRouter()
team_router.register('api/team', views.ServiceTeamAPIView)

service_person_router = routers.DefaultRouter()
service_person_router.register('api/service-person', views.ServicePersonAPIView)

personnel_urls = [
    url(r'^service-person-create/?$', views.ServicePersonCreateView.as_view(), 
        name='service-person-create'),
    url(r'^service-person-update/(?P<pk>\d+)/?$', 
        views.ServicePersonUpdateView.as_view(), name='service-person-update'),
    url(r'^service-person-dashboard/(?P<pk>\d+)/?$', 
        views.ServicePersonDashboardView.as_view(), name='service-person-dashboard'),
    url(r'^service-person-list/?$', views.ServicePersonListView.as_view(), 
        name='service-person-list'),
    url(r'^team-create/?$', views.ServiceTeamCreateView.as_view(), 
        name='team-create'),
    url(r'^team-update/(?P<pk>\d+)/?$', views.ServiceTeamUpdateView.as_view(), 
        name='team-update'),
    url(r'^team-detail/(?P<pk>\d+)/?$', views.ServiceTeamDetailView.as_view(), 
        name='team-detail'),
    url(r'^team-list/?$', views.ServiceTeamListView.as_view(), name='team-list'),
] + team_router.urls + service_person_router.urls
