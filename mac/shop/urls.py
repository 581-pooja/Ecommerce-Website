from django.urls import path
from . import views

urlpatterns = [
    # from mac.urls comes to views , from views for " " goes to views.index
    path("", views.index, name="ShopHome"),
]
