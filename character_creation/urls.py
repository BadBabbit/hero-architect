from django.urls import path

from . import views

urlpatterns = [
    path('create/', views.create_character, name='create_character'),
    path('mycharacters/', views.my_characters, name='my_characters'),
    path('mycharacters/<int:character_id>/', views.character_detail, name='character_detail'),
]