from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi



admin.site.site_header = 'Cyper cube Admin'
admin.site.index_title = 'Admin'

schema_view = get_schema_view(
    openapi.Info(
        title="Security cube API",
        default_version='v1',
        description="API documentation for Security Cube project",
        terms_of_service="https://www.yourproject.com/terms/",
        contact=openapi.Contact(email="contact@yourproject.com"),
        license=openapi.License(name="Your License"),
    ),
    public=True,  # Make the schema view publicly accessible
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls')),
    path('login/', include('djoser.urls.jwt')),
    path("user/", include("core.urls")),
    path("", include("Security_Cube_app.urls")),
    path("", include("subscription.urls")),
    path('documentation/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc'),

]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


