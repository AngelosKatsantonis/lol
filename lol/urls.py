from django.contrib import admin
from django.urls import path, include

import summoners.urls

urlpatterns = [
    path('summoners/', include(summoners.urls)),
    path('admin/', admin.site.urls),
]
