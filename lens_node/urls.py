from django.urls import path
from django.conf.urls import include
from rest_framework import routers
from .views import EndpointViewSet, DetectionViewSet, DetectionNewest, DetectionByDevice, DeviceList, \
    DetectionByDeviceNewest

router = routers.DefaultRouter()
router.register('endpoint', EndpointViewSet)
router.register('store', DetectionViewSet)
router.register('newest', DetectionNewest)
router.register('device', DetectionByDevice)
router.register('device-newest', DetectionByDeviceNewest)

urlpatterns = [
    path('', include(router.urls)),
    path('device-list/', DeviceList.as_view(), name='device-list'),
]
