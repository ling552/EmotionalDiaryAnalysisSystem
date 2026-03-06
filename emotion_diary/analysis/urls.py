from django.urls import path

from . import views

urlpatterns = [
    path('', views.analysis_dashboard_view, name='analysis_dashboard'),
]
