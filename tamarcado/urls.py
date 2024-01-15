from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from rest_framework import routers
from agenda import views

router = routers.DefaultRouter()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('agenda.urls')),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
