from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

# Import untuk tampilan Web
from usermanagement_24782042.views import RegisterView as WebRegisterView
from main_app.views import CustomLoginView, CustomLogoutView

# Import untuk API
from usermanagement_24782042.api_views import RegisterView as ApiRegisterView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django_scalar.views import scalar_viewer

urlpatterns = [
    path('', include('main_app.urls')), 
    path('dashboard/', include('dashboard_24782042.urls')),
    path('api/reports/', include('main_app.urls')),
    
    # --- AUTENTIKASI WEB ---
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('register/', WebRegisterView.as_view(), name='register'),
    
    # --- ADMIN ---
    path('admin/', admin.site.urls),
    
    # --- API ---
    path('api/', include('main_app.api_urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/', ApiRegisterView.as_view(), name='auth_register'),
    
    # --- DOKUMENTASI API ---
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/scalar/', scalar_viewer, name='scalar-docs'),
]