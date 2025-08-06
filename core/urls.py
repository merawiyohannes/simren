from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home_view'),
    path('detail/<int:item_id>', views.detail_view, name='detail_view'),
    path('search/', views.search_products, name='search_products'),
    
]
