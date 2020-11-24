from django.contrib import admin
from django.urls import path, include

import summoners.urls
import game_assets.urls

urlpatterns = [
    path('summoners/', include(summoners.urls)),
    path('', include(game_assets.urls)),
    path('admin/', admin.site.urls),
]
