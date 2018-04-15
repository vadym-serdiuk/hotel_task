"""hotel_task URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path, include
from rest_framework import routers
from rest_framework.documentation import include_docs_urls

from hotel_task.api.config.views import ConfigViewSet
from hotel_task.api.reservation.views import ReservationViewSet

router = routers.DefaultRouter()
router.register(r'config', ConfigViewSet)
router.register(r'reservation', ReservationViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('docs/', include_docs_urls(title='Hotel API', public=True)),
    path('api-auth/', include('rest_framework.urls')),
    path('', include(router.urls)),
]
