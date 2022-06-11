"""boreco URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import to include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Boreco API",
        default_version="v1"
    ),
    public=True,
    permission_classes=(permissions.AllowAny,)
)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('web-api/', schema_view.with_ui('swagger', cache_timeout=0)),
    path('web-api/user/', include('user.urls', namespace='user')),
    path('web-api/client/', include('client.urls', namespace='client')),
    path('web-api/dividend/', include('dividend.urls', namespace='dividend')),
    path('web-api/clientAssignment/', include('clientAssignment.urls', namespace='clientAssignment')),
    path('web-api/accountStatus/', include('accountStatus.urls', namespace='accountStatus')),
    path('web-api/accountStatusDeficitTotal/', include('accountStatusDeficitTotal.urls', namespace='accountStatusDeficitTotal')),
    path('web-api/accountStatusDeficit/', include('accountStatusDeficit.urls', namespace='accountStatusDeficit')),
    path('web-api/accountStatement/', include('accountStatement.urls', namespace='accountStatement')),
    path('web-api/vatpastrecord/', include('vatpastrecord.urls', namespace='vatpastrecord')),
    path('web-api/vatCurrent/', include('vatCurrent.urls', namespace='vatCurrent')),
    path('web-api/api.json/', schema_view.without_ui(cache_timeout=0), name='schema-swagger-ui'),
    path('web-api/tingsling/', include('tinglysning.urls', namespace='tinglysning')),
    path('web-api/eindkomst/', include('eindkomst.urls', namespace='eindkomst')),
    path('web-api/skattekonto/', include('Skattekonto.urls', namespace='Skattekonto')),
    path('web-api/vataccountinfo/', include('vataccountinfo.urls', namespace='vataccountinfo')),
    path('web-api/virkinfo/', include('virkinfo.urls', namespace='virkinfo')),
    path('web-api/taxreturn/', include('taxreturn.urls', namespace='virkinfo')),
]

if bool(settings.DEBUG):
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'utils.views.error_404'
handler500 = 'utils.views.error_500'
