from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include(('log_keepers.urls', "log_keepers"), namespace='log_keepers')),
    path('users/',include(('users.urls','users'),namespace='users')),
    path('admin/', admin.site.urls),
]
