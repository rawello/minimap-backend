from PIL import Image, ImageDraw

def routing(build, floors, destinations, destTo, destFrom, folder_path):
    class Node:  # создаем класс для наших точек которые будем проходить
        def __init__(self, parent=None, position=None):
            self.parent = parent  # не меняем
            self.position = position  # тоже

            self.g = 0  # стоимость движения от начального узла до текущего не важно
            self.h = 0  # эвристическая оценка расстояния до цели это тоже нам не надо
            self.f = 0  # сумма g и h туда его нафиг

        # переопределяем операторы сравнения для сортировки узлов по f значению
        # типа больше меньше или равно для кратчейшего пути
        def __eq__(self, other):
            return self.position == other.position

        def __lt__(self, other):
            return self.f < other.f

        def __gt__(self, other):
            return self.f > other.f

    # пишем функцию для поиска пути с помощью алгоритма A*
    def astar(maze, start, end):
        # инициализируем начальный и конечный точечки
        start_node = Node(None, start)
        start_node.g = start_node.h = start_node.f = 0
        end_node = Node(None, end)
        end_node.g = end_node.h = end_node.f = 0

        # инициализируем список открытых(не прошли) и закрытых(прошли) узлов
        open_list = []
        closed_list = []

        # добавляем начальный узел в список открытых
        open_list.append(start_node)

        # запускаем цикл поиска пути, пока список открытых узлов не пуст
        while len(open_list) > 0:

            # ищем узел с наименьшим f значением в списке открытых узлов
            current_node = open_list[0]
            current_index = 0
            for index, node in enumerate(open_list):
                if node.f < current_node.f:
                    current_node = node
                    current_index = index

            # переносим текущий узел из списка открытых в список закрытых
            open_list.pop(current_index)
            closed_list.append(current_node)

            # если текущий узел - тот который ищем, конечная так сказать
            if current_node == end_node:
                path = []  # списочек для пути который вернем
                current = current_node
                while current is not None:  # пока не кончится наш массивчик с путек который самый дешевый и быстрый
                    path.append(current.position)  # складываем его в выходной путь
                    current = current.parent
                return path[::-1]  # возвращаем путь в обратном порядке

            # генерируем соседние узлы для текущего узла(шагаем в стороны)
            neighbors = []
            for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]:

                node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[
                    1])  # создаем новую точку с новыми координатами
                if (node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (
                        len(maze) - 1) or  # проверяем лежит ли она в пределах карты
                        node_position[1] < 0):
                    continue
                if maze[node_position[1]][node_position[0]] != 1:  # если не стена, то шагаем
                    new_node = Node(current_node, node_position)
                    neighbors.append(new_node)

            for neighbor in neighbors:

                if neighbor in closed_list:  # если точку прошли
                    continue
                    # у нас стоимости для галочки так сказатб
                neighbor.g = current_node.g + 1  # стоимость движения от начального узла до текущего
                neighbor.h = ((neighbor.position[0] - end_node.position[0]) ** 2) + (
                        (neighbor.position[1] - end_node.position[1]) ** 2)  # эвристическая оценка расстояния до цели
                neighbor.f = neighbor.g + neighbor.h  # сумма g и h

                if neighbor in open_list and neighbor.f >= current_node.f:  # если точка есть или мы ее еще не прошли
                    continue  # скипаем

                # добавляем соседний узел в список открытых узлов
                open_list.append(neighbor)

    def createMatrix(x):
        for k in range(x):
            k += 1
            file = open(f"{folder_path}/{k}-{build}-matrix.txt", "w")  # файл матрицы
            im = Image.open(f"{folder_path}/{k}-{build}.png")  # картинка, которую преобразовываем

            if im.mode != 'RGB':
                im = im.convert('RGB')

            for i in range(im.size[0]):
                for j in range(im.size[1]):
                    if im.getpixel((j, i)) == (255, 255, 255):  # если белый цвет - пустота
                        file.write("0 ")
                    elif im.getpixel((j, i)) == (0, 0, 0):  # если черный - стена
                        file.write("1 ")
                    elif im.getpixel((j, i)) == (63, 72, 204):  # точка старта-конца
                        file.write("2 ")
                    elif im.getpixel((j, i)) == (14, 209, 69):  # лестница
                        file.write("3 ")
                    else:  # любой другой - стена
                        file.write("1 ")
                file.write("\n")
            file.close()

    allMazes = []  # массив для всех матриц
    # преобразовываем пикчу в матрицу
    createMatrix(
        len(floors))  # передаем в создание матрицы количество этажей(это кста самое долгое действие - перевод пнг в тхт)

    def getMazes():
        for i in range(len(floors)):
            i += 1
            maze = []
            with open(f"{folder_path}/{i}-{build}-matrix.txt", 'r') as f:
                for line in f:
                    maze.append(
                        list(map(int,
                                 line.split())))  # считываем картинку без пробелов и складываем в матрицу так сказать
            allMazes.append(maze)

    getMazes()

    if destinations.get(destFrom)[0] != destinations.get(destTo)[0]:
        # если несколько этажей
        # массивы для лестниц, маршрутов лестниц
        coordStairsX = []
        coordStairsY = []
        allPathes = []

        for coor in range(len(allMazes[destinations.get(destFrom)[
                                           0] - 1])):  # разбираем массив матриц, ищем тройки и записываем в массивы
            for i in range(len((allMazes[destinations.get(destFrom)[0] - 1])[coor])):
                if (allMazes[destinations.get(destFrom)[0] - 1])[coor][i] == 3:
                    coordStairsX.append(coor)
                    coordStairsY.append(i)

        for stairs in range(len(coordStairsX)):
            path = astar(allMazes[destinations.get(destFrom)[0] - 1], tuple(destinations.get(destFrom)[1]),
                         tuple((coordStairsY[stairs], coordStairsX[stairs])))
            #print(len(path))
            allPathes.append(path)

        def minMatrix(temp):
            sn = len(temp[0])
            res = 0
            for i in range(len(temp)):
                if len(temp[i]) < sn:
                    res = i
            return res

        if minMatrix(allPathes) is not None:  # если путь найден
            with Image.open(
                    f"{folder_path}/{destinations.get(destFrom)[0]}-{build}.png") as im:  # выбираем на основе какой пикчи будем рисовать
                if im.mode != 'RGB':
                    im = im.convert('RGB')
                draw = ImageDraw.Draw(im)
                for i in allPathes[minMatrix(allPathes)]:
                    draw.point(i, (128, 128, 128))  # чиркаем маршрут серым по координатам из алгоритма
                im.save(f"{folder_path}/{destinations.get(destFrom)[0]}-{build}-routed.png",
                        "PNG")  # сохраняем пикчу в другой файл чтобы исходник жил
                #print("успешно, длина пути до лестницы", len(min(allPathes)), "шага")
        else:  # если путь не найден
            print(None)  # сосем бибу
            return False

        path = astar(allMazes[destinations.get(destTo)[0] - 1], tuple(destinations.get(destTo)[1]),
                     (coordStairsY[minMatrix(allPathes)], coordStairsX[minMatrix(allPathes)]))
        if path is not None:  # если путь найден
            with Image.open(
                    f"{folder_path}/{destinations.get(destTo)[0]}-{build}.png") as im:  # выбираем на основе какой пикчи будем рисовать
                if im.mode != 'RGB':
                    im = im.convert('RGB')
                draw = ImageDraw.Draw(im)
                for i in path:
                    draw.point(i, (128, 128, 128))  # чиркаем маршрут серым по координатам из алгоритма
                im.save(f"{folder_path}/{destinations.get(destTo)[0]}-{build}-routed.png",
                        "PNG")  # сохраняем пикчу в другой файл чтобы исходник жил
                #print("успешно, длина пути до точки", len(path), "шага")
                return True
        else:  # если путь не найден
            print(None)  # сосем бибу
            return False

    else:
        # просто рисуем маршрут по этажу
        path = astar(allMazes[destinations.get(destTo)[0] - 1], tuple(destinations.get(destTo)[1]),
                     tuple(destinations.get(destFrom)[1]))
        if path is not None:  # если путь найден
            with Image.open(
                    f"{folder_path}/{destinations.get(destTo)[0]}-{build}.png") as im:  # выбираем на основе какой пикчи будем рисовать
                if im.mode != 'RGB':
                    im = im.convert('RGB')
                draw = ImageDraw.Draw(im)
                for i in path:
                    draw.point(i, (128, 128, 128))  # чиркаем маршрут серым по координатам из алгоритма
                im.save(f"{folder_path}/{destinations.get(destTo)[0]}-{build}-routed.png",
                        "PNG")  # сохраняем пикчу в другой файл чтобы исходник жил
                # print("успешно, длина пути до точки", len(path), "шага")
                return True
        else:  # если путь не найден
            print(None)  # сосем бибу
            return False