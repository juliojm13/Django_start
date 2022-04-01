from django.urls import path

import ordersapp.views as ordersapp_views

app_name = 'ordersapp'

urlpatterns = [
    path('forming/complete/<int:pk>', ordersapp_views.forming_complete, name='order_forming_complete'),
    path('', ordersapp_views.OrderListView.as_view(), name='orders_list'),
    path('create/', ordersapp_views.OrderCreateView.as_view(), name='order_create'),
    path('update/<int:pk>/', ordersapp_views.OrderUpdateView.as_view(), name='order_update'),
    path('delete/<int:pk>/', ordersapp_views.OrderDeleteView.as_view(), name='order_delete'),
    path('detail/<int:pk>/', ordersapp_views.OrderDetailView.as_view(), name='order_detail'),
]