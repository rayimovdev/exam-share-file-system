from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenRefreshView

schema_view = get_schema_view(
    openapi.Info(
        title="Share file system API",
        default_version='v0.5.0',
        description="Test API",
        contact=openapi.Contact(email='rayimovdev@gmail.com'),
        terms_of_service="https://www.google.com/policies/terms/",
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/', include('users.api.urls.registration')),
    path('api/file/', include('files.api.urls.file_upload')),
    path('api/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)