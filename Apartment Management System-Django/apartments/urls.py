from django.urls import path

from . import manager_views, views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("request/", views.submit_request, name="submit_request"),
    path("manager/", manager_views.manager_dashboard, name="manager_dashboard"),
    path("manager/payments/<int:pk>/paid/", manager_views.mark_paid, name="mark_paid"),
    path("manager/requests/<int:pk>/<slug:decision>/",
         manager_views.decide_request, name="decide_request"),
]
