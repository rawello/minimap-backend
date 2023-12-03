from django.urls import path, include
from djangoclient import mobileOps, frontOps

urlpatterns = [
    path('login', frontOps.login),
    path('register', frontOps.register),
    path('allMaps/<path:loginuser>', frontOps.allMaps),
    #path('saveFrontObj', frontOps.saveFrontObj),
    path('editRoute', frontOps.editRoute),
    path('deleteRoute', frontOps.deleteRoute),
    path("generateQR/<path:build>/<path:start>", frontOps.generateQR),
    path('getObj/<path:loginuser>/<path:build>', frontOps.getObj),
    path('addRouteToDbFromFront', frontOps.addRouteToDbFromFront),

    path('generateImages/<path:build>/<path:destinationFrom>/<path:destinationTo>', mobileOps.generate_images),
    path('connectWithMobile/<path:build>', mobileOps.connectWithMobile),
    path('getBuildings', mobileOps.getBuilding),
    path('getListOfRooms/<path:build>', mobileOps.getListOfRooms),
]