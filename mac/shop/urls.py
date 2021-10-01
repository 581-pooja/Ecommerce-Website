from django.urls import path
from . import views

urlpatterns = [
    # from mac.urls comes to views , from views for " " goes to views.index
    path("", views.index, name="ShopHome"),
    path("about/", views.about, name="AboutUs"),
    path("contact/", views.contact, name="ContactUS"),
    path("tracker/", views.tracker, name="Tracking Status"),
    path("search/", views.search, name="Search"),
    path("products/<int:myid>", views.productView, name="ProductView"),
    path("checkout/", views.checkout, name="CheckOut"),
    path("success/", views.success, name="Success"),
]
