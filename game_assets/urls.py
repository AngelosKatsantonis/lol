from django.urls import path

from .views import champions, champion_by_name

urlpatterns = [
    path('', champions, name='champions'),
    path('<name>/', champion_by_name, name='champion_by_name'),
]
