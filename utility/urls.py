from django.urls import path
from . import views

urlpatterns = [
    path("add_item/", views.add_item_view, name='add_item_view'),
    path("edit/<int:id>", views.edit_view, name='edit_view'),
    path("delete/<int:id>", views.delete_view, name='delete_view'),
]
