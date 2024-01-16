from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls import include
from rest_framework import routers
from agenda import views
from django.contrib.staticfiles.views import serve


router = routers.DefaultRouter()

def return_static(request, path, insecure=True, **kwargs):
    return serve(request, path, insecure, **kwargs)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('agenda.urls')),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    re_path(r'^search_danfe/static/(?P<path>.*)$', return_static, name='static')
]
