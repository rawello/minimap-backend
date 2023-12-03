import inspect
import shutil
import json
import os
import random
import segno
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from djangoclient.models import User, Maps

def allMaps(request, loginuser):
    # получаем все роуты созданные пользователем
    builds = Maps.objects.all()
    response = []
    output = {}
    for obj in builds:
        if obj.login == loginuser:
            response.append(obj.build)
    for i in range(len(response)):
        output[i + 1] = response[i]
    return JsonResponse(output)


def getObj(request, loginuser, build):
    try:
        obj = Maps.objects.get(build=build, login=loginuser)
        output_json = {
            "build": f'{build}',
            "login": f'{loginuser}',
            "obj": f'{obj.obj}'
        }
        return JsonResponse(output_json)

    except Exception as e:
        print(e, inspect.stack()[0][3])
        return HttpResponse(400)


@csrf_exempt
def addRouteToDbFromFront(request):
    data = json.loads(request.body)
    build = data['build']
    rooms = data['rooms']
    loginuser = data['login']
    svg_maps = data['svg']
    obj = data['obj']
    try:
        currMap = Maps(svg=svg_maps, rooms=rooms, login=loginuser, build=build, obj=obj)
    except Exception as e:
        print(e, inspect.stack()[0][3])
        return HttpResponse(400)
    else:
        currMap.save()
        return HttpResponse(200)

@csrf_exempt
def editRoute(request):
    data = json.loads(request.body)
    old_name = data['build']
    build = data['build_new']
    rooms = data['rooms']
    loginuser = data['login']
    svg_maps = data['svg']
    obj = data['obj']
    try:
        # ищем, удаляем, создаем
        currObj = Maps.objects.get(build=old_name, login=loginuser)
        currObj.delete()
        newObj = Maps(svg=svg_maps, rooms=rooms, login=loginuser, build=build, obj=obj)
        newObj.save()
    except Exception as e:
        print(e, inspect.stack()[0][3])
        return HttpResponse(400)
    else:
        return HttpResponse(200)

def deleteRoute(request):
    # ищем, удаляем
    data = json.loads(request.body)
    build = data['build']
    loginuser = data['login']
    try:
        currMap = Maps.objects.get(build=build, login=loginuser)
        currMap.delete()
    except Exception as e:
        print(e, inspect.stack()[0][3])
        return HttpResponse(400)
    else:
        return HttpResponse(200)

def generateQR(request, build, start):
    qrcode = segno.make_qr(f"{build}///{start}")

    folder_path = f'{random.randint(0, 10000000)}'
    os.makedirs(folder_path, exist_ok=True)

    img_path = f"{folder_path}/{build}-qr.svg"
    qrcode.save(img_path, scale=10)

    with open(img_path, 'r') as file:
        svg = file.read()
    shutil.rmtree(f'{folder_path}')

    return HttpResponse(svg, content_type='image/svg+xml')


@csrf_exempt
def login(request):
    # получаем жсон и чекаем есть ли в бд
    data = json.loads(request.body)
    loginuser = data['login']
    password = data['password']
    try:
        users = User.objects.get(login=f'{loginuser}', password=f'{password}')
    except Exception as e:
        print(e, inspect.stack()[0][3])
        return HttpResponse(400)
    else:
        return HttpResponse(200)


@csrf_exempt
def register(request):
    # получаем жсон и регаем в бд
    data = json.loads(request.body)
    loginuser = data['login']
    password = data['password']

    users = User.objects.all()
    for user in users:
        if loginuser == user.login:
            print("уже есть такое")
            return HttpResponse(400)

    newuser = User(login=f'{loginuser}', password=f'{password}')
    newuser.save()

    return HttpResponse(200)
