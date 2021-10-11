from django.urls import path
from .views import index, memory_detail, memory_add, memory_data

urlpatterns = [
    path('', index, name='index'),
    path('memory/detail/<int:pk>/', memory_detail, name='memory_detail'),
    path('memory/add/', memory_add, name='memory_add'),
    path('memory/data/', memory_data, name='memory_data'),
]
