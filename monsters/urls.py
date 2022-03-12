from django.urls import path

from . import views

# /monsters/...
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:monster_id>/', views.detail, name='detail')
]