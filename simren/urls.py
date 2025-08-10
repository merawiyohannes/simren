
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('', include('cart.urls')),
    path('', include('authentication.urls')),
    path('', include('utility.urls')),
    path('', include('dashboard.urls')),
    
]
