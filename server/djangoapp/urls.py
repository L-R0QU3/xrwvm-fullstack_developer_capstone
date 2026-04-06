from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('login', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('register', views.registration, name='register'),
    path('get_cars', views.get_cars, name='get_cars'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)