from django.urls import path
from . import views

app_name = "livestock"

urlpatterns = [
    path("", views.LivestockListView.as_view(), name="list"),
    path("<slug:slug>/", views.LivestockDetailView.as_view(), name="detail"),
]
