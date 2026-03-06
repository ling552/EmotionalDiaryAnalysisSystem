from django.urls import path

from . import views

urlpatterns = [
    path('', views.diary_list_view, name='diary_list'),
    path('add/', views.diary_add_view, name='diary_add'),
    path('<int:diary_id>/edit/', views.diary_edit_view, name='diary_edit'),
    path('<int:diary_id>/delete/', views.diary_delete_view, name='diary_delete'),
]
