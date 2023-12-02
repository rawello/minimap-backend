from django.urls import path, include
from djangoclient import mobileOps, frontOps

urlpatterns = [
    path('login', frontOps.login),
    path('register', frontOps.register),
    path('generateImages/<path:build>/<path:destinationFrom>/<path:destinationTo>', mobileOps.generate_images),
    path('connectWithMobile/<path:build>', mobileOps.connectWithMobile),
    path('addRouteToDbFromFront', frontOps.addRouteToDbFromFront),
    path('getBuildings', mobileOps.getBuilding),
    path('allRoutes', frontOps.allRoutes),
    path('editRoute', frontOps.editRoute),
    path('deleteRoute', frontOps.deleteRoute),
    path("generateQR/<path:build>/<path:start>", frontOps.generateQR),
    path('getRoute/<path:loginuser>/<path:build>', frontOps.getRoute),
]