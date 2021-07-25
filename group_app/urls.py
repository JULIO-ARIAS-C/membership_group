from django.urls import path
from . import views


urlpatterns = [
    path('main',views.main),
    path('create_user',views.create_user),
    path('create_org', views.create_org),
    path('/groups/<int:organization_id>',views.view_group),
    path('groups', views.groups),
    path('login',views.login),
    path('logout',views.logout),
]