"""final URL Configuration

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
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from rest_framework import routers

from authentication.views import Login, Logout, Registration
import cinema.views as cls
from rest_framework.authtoken import views
from API.resorces import FilmViewSet, PurchaseViewSet

router = routers.DefaultRouter()
router.register(r'api-films', FilmViewSet)
router.register(r'api-purchases', PurchaseViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('registration/', Registration.as_view(), name='registration'),

    path('', cls.SeancesListView.as_view(), name='index'),
    path('films/', cls.FilmsListView.as_view(), name='list_films'),
    path('rooms/', cls.RoomsListView.as_view(), name='list_rooms'),

    path('create_seance/', cls.SeanceCreateView.as_view(), name='create_seance'),
    path('create_room/', cls.RoomCreateView.as_view(), name='create_room'),
    path('create_film/', cls.FilmCreateView.as_view(), name='create_film'),
    path('create_purchase/', cls.PurchaseCreateView.as_view(), name='create_purchase'),

    path('update_seance/<int:pk>/', cls.SeanceUpdateView.as_view(), name='update_seance'),
    path('update_room/<int:pk>/', cls.RoomUpdateView.as_view(), name='update_room'),
    path('update_film/<int:pk>/', cls.FilmUpdateView.as_view(), name='update_film'),

    path('api-auth/', include('rest_framework.urls')),
    path('api-token-auth/', views.obtain_auth_token),
    path('', include(router.urls)),
]
