from django.urls import path
from . import views
urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard_view'),
    path('dashboard/seen', views.make_orders_seen, name='make_orders_seen'),
    path('order/unseen/', views.unseen_orders_count, name='unseen_orders_view')

]
