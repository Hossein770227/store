
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', include('store.urls')),
    path('', include('website.urls')),
    path('__debug__/', include('debug_toolbar.urls')),
]