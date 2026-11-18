from django.urls import path

from . import manager_views, views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("manager/", manager_views.manager_dashboard, name="manager_dashboard"),
    path("manager/payments/<int:pk>/paid/", manager_views.mark_paid, name="mark_paid"),
]
