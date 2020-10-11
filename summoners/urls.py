from django.urls import path

from .views import leagues, profile, search, update

urlpatterns = [
    path('leagues/<region>/', leagues, name='leagues_by_region'),
    path('leagues/', leagues, name='leagues'),
    path('profile/<id>/', profile, name='profile'),
    path('search/', search, name='search'),
    path('update/<id>/', update, name='update'),
]
