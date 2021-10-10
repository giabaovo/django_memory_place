from django.urls import path
from .views import index, memory_detail

urlpatterns = [
    path('', index, name='index'),
    path('memory/detail/<int:pk>/', memory_detail, name='memory_detail'),
]
