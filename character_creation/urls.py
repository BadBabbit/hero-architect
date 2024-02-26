from django.urls import path

from . import views

urlpatterns = [
    path('', views.create_character, name='create_character'),
    path('', views.my_characters, name='my_characters'),
    path('mycharacters/<str:character_name>/', views.character_detail, name='character_detail'),
]