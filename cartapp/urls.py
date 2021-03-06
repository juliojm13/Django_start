from django.urls import path

import cartapp.views as cartapp_views

app_name = 'cartapp'

urlpatterns = [
    path('', cartapp_views.cart, name='cart'),
    path('add/<int:pk>', cartapp_views.add_to_cart, name='add_to_cart'),
    path('remove/<int:pk>', cartapp_views.remove_from_cart, name='remove_from_cart'),
    path('product/<int:pk>', cartapp_views.adding_product, name='adding_product'),
    path('edit/<int:pk>/<int:quantity>/', cartapp_views.cart_edit, name='edit')

]
