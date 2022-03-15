from django.urls import path

import mainapp.views as mainapp_views

app_name = 'mainapp'

urlpatterns = [
   path('', mainapp_views.products, name='index'),
   path('category/<int:pk>/', mainapp_views.products_category, name='category'),
   path('category/<int:pk>/page/<int:page>/', mainapp_views.products_category, name='page'),
   path('category/all/', mainapp_views.products_category, name='all'),
   path('category/all/page/<int:page>/', mainapp_views.products_category, name='page_all'),
]