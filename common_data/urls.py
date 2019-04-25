from django.urls import include, re_path

from common_data import views
workflow = views.WorkFlowView.as_view()
urlpatterns = [
    re_path(r'^workflow/?$', workflow, name="workflow"),
    re_path(r'^react-test/?$', views.ReactTestView.as_view(), 
        name="react-test"),    
    re_path(r'^about/?$', views.AboutView.as_view(), name="about"),
    re_path(r'^logo-url/?$', views.get_logo_url, name='logo-url'),
    re_path(r'^organization/create/?$', views.OrganizationCreateView.as_view(), 
        name='organization-create'),
    re_path(r'^organization/list/?$', views.OrganizationListView.as_view(), 
        name='organization-list'),
    re_path(r'^organization/update/(?P<pk>[\d]+)/?$', views.OrganizationUpdateView.as_view(), 
        name='organization-update'),
    re_path(r'^organization/detail/(?P<pk>[\d]+)/?$', views.OrganizationDetailView.as_view(), 
        name='organization-detail'),
    re_path(r'^individual/create/?$', views.IndividualCreateView.as_view(), 
        name='individual-create'),
    re_path(r'^individual/list/?$', views.IndividualListView.as_view(), 
        name='individual-list'),
    re_path(r'^individual/update/(?P<pk>[\d]+)/?$', views.IndividualUpdateView.as_view(), 
        name='individual-update'),
    re_path(r'^individual/detail/(?P<pk>[\d]+)/?$', views.IndividualDetailView.as_view(), 
        name='individual-detail'),
    re_path(r'^config/(?P<pk>[\d]+)/?$', views.GlobalConfigView.as_view(), 
        name='config'),
    re_path(r'^email/?$', views.SendEmail.as_view(), 
        name='email'),
    re_path(r'^authenticate/?$', views.AuthenticationView.as_view(), 
        name='authenticate'),
    re_path(r'^api/current-user/?$', views.get_current_user,
        name='api-current-user'),
    re_path(r'^license-error-page/?$', views.LicenseErrorPage.as_view(),
        name='license-error-page'),
    re_path(r'^license-error/features/?$', views.LicenseFeaturesErrorPage.as_view(),
        name='license-error-features'),
    re_path(r'^license-error/users/?$', views.UsersErrorPage.as_view(),
        name='license-error-users'),
    re_path(r'^api/users/?$', views.UserAPIView.as_view(), name='api-users'),
    re_path(r'^create-note/?$', views.create_note, name='create-note'),
    re_path(r'^models/get-latest/(?P<app>[\w ]+)/(?P<model_name>[\w ]+)/?$', 
        views.get_model_latest, name='get-latest-model'),
]
