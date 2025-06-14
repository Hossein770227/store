
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', include('store.urls')),
    path('', include('website.urls')),
    path('cart/', include('cart.urls')),
    path('profile/', include('dashboard.urls')),
    path("order/",include('orders.urls')),
    path('payment/', include('payment.urls')),
    # rosetta translate
    path('rosetta/', include('rosetta.urls')),
]

if settings.DEBUG:
    urlpatterns +=[path('__debug__/', include('debug_toolbar.urls')),]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)