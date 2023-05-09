from django.contrib import admin
from django.urls import path, include, re_path
from rest_auth.registration.views import VerifyEmailView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="Test License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
   #  path('api-auth/', include('rest_framework.urls')),
   #  path('rest-auth/', include('rest_auth.urls')),
   #  path('rest-auth/registration/', include('rest_auth.registration.urls')),
   #  re_path(r'^account-confirm-email/', VerifyEmailView.as_view(),
   #   name='account_email_verification_sent'),
   #  re_path(r'^account-confirm-email/(?P<key>[-:\w]+)/$', VerifyEmailView.as_view(),
   #   name='account_confirm_email'),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('auth/', include('djoser.social.urls')),
    path('store/', include('Store.urls')),
    path ('swagger/schema', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
#    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
#    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
# path('store/', include('Store.urls')),