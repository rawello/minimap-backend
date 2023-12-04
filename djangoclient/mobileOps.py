import inspect
import shutil
import os
import random
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from djangoclient.astar import routing
from djangoclient.imageOps import convert2svg, convert2png
from djangoclient.models import Maps


@csrf_exempt
def generate_images(request, build, destinationFrom, destinationTo):
    folder_path = 0
    try:
        databaseObj = Maps.objects.get(build=build)
        rooms_ll = databaseObj.rooms

        floors = []
        for i in rooms_ll.values():
            for j in i:
                if type(j) is not list:
                    floors.append(j)
        floors = list(set(floors))

        # TODO: заставить Сеню сделать произвольные точки
        # \
        # arbitraryRouteTo = data['arbitraryTo']
        # arbitraryRouteFrom = data['arbitraryFrom']
        # \
        # if arbitraryRouteTo != "None":
        #     rooms_ll["arTo"] = arbitraryRouteTo
        #     destinationTo = "arTo"
        # if arbitraryRouteFrom != "None":
        #     rooms_ll["arFrom"] = arbitraryRouteFrom
        #     destinationFrom = "arFrom"

        # создаем случайное имя папки
        while True:
            folder_path = f'{random.randint(0, 10000000)}'
            if os.path.isdir(f"{folder_path}"):
                continue
            else:
                os.makedirs(folder_path)
                break
        for i in range(len(databaseObj.svg)):
            with open(f'{folder_path}/{i + 1}-{build}.svg', 'w') as f:
                f.write(databaseObj.svg[i])
                convert2png(folder_path, f'{i + 1}-{build}.svg')
        route = routing(build, floors, rooms_ll, destinationTo, destinationFrom, folder_path)
        # вызываем метод алгоритма с рисованием
        if route:
            convert2svg(folder_path)
            # получаем список файлов в папке
            files = [file for file in os.listdir(folder_path) if "routed.svg" in file]
            floors = []
            if files:
                output_json = {
                    #"build": f'{build}',
                    "floor": [rooms_ll[destinationFrom][0], rooms_ll[destinationTo][0]]
                }
                # создаем жсон и добавляем строки в него
                for file in files:
                    with open(f'{folder_path}/{file}', 'r') as file1:
                        data = file1.read().replace('\n', '').replace('\\', '')
                    floors.append(data)
                output_json["maps"] = floors
                # отправляем жсон
                response = JsonResponse(output_json)
                print("мы в ответе")
                shutil.rmtree(f'{folder_path}')
                return response
        else:
            # в любом другом случае плохо
            print(route)
            shutil.rmtree(f'{folder_path}')
            return HttpResponse(400)
    except Exception as e:
        print(e, inspect.stack()[0][3])
        shutil.rmtree(f'{folder_path}')
        return HttpResponse(400)
    # else:
    #     print(folder_path)
    #     #shutil.rmtree(f'{folder_path}')


@csrf_exempt
def connectWithMobile(request, build):
    # ты даешь нам адрес куда тебе надо мы возвращаем адрес, этажи, комнаты, карты в свг
    try:
        obj = Maps.objects.get(build=build)
        # floors = []
        rooms = obj.rooms
        output_json = {
            "build": f'{build}',
        }
        room = []
        for i in rooms:
            room.append(i)
        #     floors.append(rooms[i][0])
        # output_json["floors"] = max(floors)
        # output_json["rooms"] = room
        output_json["maps"] = obj.svg
        return JsonResponse(output_json)
    except Exception as e:
        print(e, inspect.stack()[0][3])
        return HttpResponse(400)


def getListOfRooms(request, build):
    obj = Maps.objects.get(build=build)
    rooms = obj.rooms
    room = []
    for i in rooms:
        room.append(i)
    return JsonResponse({"rooms": room})


def getBuilding(request):
    allMaps = Maps.objects.all()
    response = []

    for building in allMaps:
        response.append(building.build)

    return JsonResponse({"buildings": response})
