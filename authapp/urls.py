from django.urls import path, re_path

import authapp.views as authapp_views

app_name = 'authapp'

urlpatterns = [
    path('login/', authapp_views.login, name='login'),
    path('logout/', authapp_views.logout, name='logout'),
    path('edit/', authapp_views.edit, name='edit'),
    path('register/', authapp_views.register, name='register'),
    re_path(r'^verify/(?P<email>.+)/(?P<activation_key>\w+)/$', authapp_views.verify, name='verify'),
]
