from django.contrib import admin
from django.urls import path, include
from usermanagement_24782042.views import RegisterView
from main_app.views import CustomLoginView, CustomLogoutView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),

    path('', include('main_app.urls')),
]