from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('account/', include('user_auth.urls')),
    path('blog/', include('blogapp.urls')),

    path('schema/', SpectacularAPIView.as_view(), name="schema"),
    path('schema/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name="swagger"),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name="redoc"),
]

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('shop/', include('shopapp.urls')),
)

if settings.DEBUG:
    urlpatterns.extend(
        static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    )

    urlpatterns.extend(
        static(settings.STATIC_URL, document_root=settings.STATIC_URL)
    )

    urlpatterns.append(
        path("__debug__/", include("debug_toolbar.urls")),
    )
