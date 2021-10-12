from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('v1/package/publish', views.publish_package, name='v1/package/publish'),
    path('v1/package/download', views.download_package, name='v1/package/download'),
]
