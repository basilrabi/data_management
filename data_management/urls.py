"""data_management URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

admin.site.site_header = 'Data Management'
admin.site.site_title = 'TMC'
admin.site.index_title = 'Data Groups'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/map/')),
    path('custom/', include('custom.urls')),
    path('inventory/', include('inventory.urls')),
    path('location/', include('location.urls')),
    path('map/', include('map.urls')),
    path('sampling/', include('sampling.urls')),
    path('shipment/', include('shipment.urls'))
]

try:
    from .developer import DEVELOPER
    if DEVELOPER:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
except:
    pass
