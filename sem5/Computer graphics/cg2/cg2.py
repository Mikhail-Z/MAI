import pygame
from pygame.locals import *

import numpy as np
import random
import math
from operator import itemgetter

x = 1
y = 1
# смещения относительно центра
offsetx = 0
offsety = 0

# дистанция до объекта
distance = 4

class Point:
    def __init__(self, x=0, y=0, z=0):
        self.x, self.y, self.z = float(x), float(y), float(z)


    def rotate_x(self, angle):
        rad = angle * math.pi / 180

        cos_a = math.cos(rad)
        sin_a = math.sin(rad)
        y = self.y * cos_a - self.z * sin_a
        z = self.y * sin_a + self.z * cos_a
        return Point(self.x, y, z)

    def rotate_y(self, angle):
        rad = angle * math.pi / 180

        cos_a = math.cos(rad)
        sin_a = math.sin(rad)
        z = self.z * cos_a - self.x * sin_a
        x = self.z * sin_a + self.x * cos_a

        return Point(x, self.y, z)

    def rotate_z(self, angle):
        rad = angle * math.pi / 180

        cosa = math.cos(rad)
        sina = math.sin(rad)
        x = self.x * cosa - self.y * sina
        y = self.x * sina + self.y * cosa
        return Point(x, y, self.z)

    # установка координат в зависимости от дистанции
    def project(self, win_width, win_height, fov, viewer_distance):
        factor = fov / (viewer_distance + self.z)

        x = self.x * factor + win_width / 2
        y = -self.y * factor + win_height / 2

        return Point(x, y, self.z)

# список вершин, которые определяются тремя координатами
verticies = [
    Point(offsetx, offsety-y, x*np.sin(36*np.pi/180)),
    Point(offsetx+x*np.sin(54*np.pi/180), offsety-y, 0),
    Point(offsetx-x*np.sin(54*np.pi/180), offsety-y, 0),
    Point(offsetx+x/2, offsety-y, -x*np.sin(np.pi*72/180)),
    Point(offsetx-x/2, offsety-y, -x*np.sin(np.pi*72/180)),
    Point(offsetx, offsety+y, x*np.sin(36*np.pi/180)),
    Point(offsetx+x*np.sin(54*np.pi/180), offsety+y, 0),
    Point(offsetx-x*np.sin(54*np.pi/180), offsety+y, 0),
    Point(offsetx+x/2, offsety+y, -x*np.sin(np.pi*72/180)),
    Point(offsetx-x/2, offsety+y, -x*np.sin(np.pi*72/180))
]

# плоскости хранят номера вершин, которые их образуют
surfaces = (
    (1, 0, 2, 4, 3),
    (1, 0, 5, 6),
    (0, 2, 7, 5),
    (1, 3, 8, 6),
    (2, 4, 9, 7),
    (3, 4, 9, 8),
    (5, 6, 8, 9, 7)
)

# цвета для каждой плоскости
colors = [[random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)],
          [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)],
          [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)],
          [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)],
          [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)],
          [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)],
          [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]]


angle_x, angle_y, angle_z = 0, 0, 0


def rotate(screen, alpha, param):
    global verticies

    # здесь хранятся измененные вершины
    tVertices = []
    global angle_x, angle_y, angle_z
    for vertex in verticies:
        # повернуть вершины
        rotation = vertex.rotate_x(angle_x).rotate_y(angle_y).rotate_z(angle_z)
        # изменить вершины в зависимости от дистанции
        projection = rotation.project(screen.get_width(), screen.get_height(), 256, distance)
        tVertices.append(projection)
    avgZ = []
    i = 0
    # алгоритм художника для удаления невидимых линий
    for f in surfaces:
        if len(f) == 4:
            # считаем координату z середины плоскости
            z = (tVertices[f[0]].z + tVertices[f[1]].z + tVertices[f[2]].z + tVertices[f[3]].z) / 4.0
        else:
            z = (tVertices[f[0]].z + tVertices[f[1]].z + tVertices[f[2]].z + tVertices[f[3]].z + tVertices[f[4]].z) / 5.0
        avgZ.append([i, z])
        i = i + 1
    # отсортировали по среднем значению плоскости по убыванию
    for zVal in sorted(avgZ, key=itemgetter(1), reverse=True):
        print(zVal[1])
        fIndex = zVal[0]
        f = surfaces[fIndex]
        if len(f) == 4:
            pointList = [(tVertices[f[0]].x, tVertices[f[0]].y), (tVertices[f[1]].x, tVertices[f[1]].y),
                         (tVertices[f[1]].x, tVertices[f[1]].y), (tVertices[f[2]].x, tVertices[f[2]].y),
                         (tVertices[f[2]].x, tVertices[f[2]].y), (tVertices[f[3]].x, tVertices[f[3]].y),
                         (tVertices[f[3]].x, tVertices[f[3]].y), (tVertices[f[0]].x, tVertices[f[0]].y)]
        else:
            pointList = [(tVertices[f[0]].x, tVertices[f[0]].y), (tVertices[f[1]].x, tVertices[f[1]].y),
             (tVertices[f[1]].x, tVertices[f[1]].y), (tVertices[f[2]].x, tVertices[f[2]].y),
             (tVertices[f[2]].x, tVertices[f[2]].y), (tVertices[f[3]].x, tVertices[f[3]].y),
             (tVertices[f[3]].x, tVertices[f[3]].y), (tVertices[f[4]].x, tVertices[f[4]].y),
             (tVertices[f[4]].x, tVertices[f[4]].y), (tVertices[f[0]].x, tVertices[f[0]].y)]

        pygame.draw.polygon(screen, colors[fIndex], pointList)

    if (param == "UP"):
        angle_x += 2
    elif (param == "DOWN"):
        angle_x -= 2
    elif (param == "LEFT"):
        angle_y += 2
    elif (param == "RIGHT"):
        angle_y -= 2

    # обновляем экран
    pygame.display.flip()
    screen.fill((100, 100, 100))

# аналогично предыдущей функции rotate
def renderFigure(screen):
    global angle_x, angle_y, angle_z
    tVertices = []

    for vertex in verticies:
        rotation = vertex.rotate_x(angle_x).rotate_y(angle_y).rotate_z(angle_z)
        projection = rotation.project(screen.get_width(), screen.get_height(), 256, distance)
        tVertices.append(projection)

    avgZ = []
    i = 0
    for f in surfaces:
        if len(f) == 4:
            z = (tVertices[f[0]].z + tVertices[f[1]].z + tVertices[f[2]].z + tVertices[f[3]].z) / 4.0
        else:
            z = (
                tVertices[f[0]].z + tVertices[f[1]].z + tVertices[f[2]].z + tVertices[f[3]].z + tVertices[f[4]].z) / 5.0
        avgZ.append([i, z])
        i = i + 1

    for zVal in sorted(avgZ, key=itemgetter(1), reverse=True):
        fIndex = zVal[0]
        f = surfaces[fIndex]
        if len(f) == 4:
            pointList = [(tVertices[f[0]].x, tVertices[f[0]].y), (tVertices[f[1]].x, tVertices[f[1]].y),
                         (tVertices[f[1]].x, tVertices[f[1]].y), (tVertices[f[2]].x, tVertices[f[2]].y),
                         (tVertices[f[2]].x, tVertices[f[2]].y), (tVertices[f[3]].x, tVertices[f[3]].y),
                         (tVertices[f[3]].x, tVertices[f[3]].y), (tVertices[f[0]].x, tVertices[f[0]].y)]
        else:
            pointList = [(tVertices[f[0]].x, tVertices[f[0]].y), (tVertices[f[1]].x, tVertices[f[1]].y),
                         (tVertices[f[1]].x, tVertices[f[1]].y), (tVertices[f[2]].x, tVertices[f[2]].y),
                         (tVertices[f[2]].x, tVertices[f[2]].y), (tVertices[f[3]].x, tVertices[f[3]].y),
                         (tVertices[f[3]].x, tVertices[f[3]].y), (tVertices[f[4]].x, tVertices[f[4]].y),
                         (tVertices[f[4]].x, tVertices[f[4]].y), (tVertices[f[0]].x, tVertices[f[0]].y)]

        pygame.draw.polygon(screen, colors[fIndex], pointList)

    pygame.display.flip()

def main():
    pygame.init()
    i = 0
    win_width = 800
    win_height = 600
    screen = pygame.display.set_mode((win_width, win_height))
    screen.fill((100, 100, 100))
    renderFigure(screen)
    pygame.key.set_repeat(1,100)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    rotate(screen, 5*np.pi/180, 'LEFT')
                if event.key == pygame.K_RIGHT:
                    rotate(screen, -5*np.pi/180, 'RIGHT')
                if event.key == pygame.K_UP:
                    rotate(screen, 5*np.pi/180, 'UP')
                if event.key == pygame.K_DOWN:
                    rotate(screen, -5*np.pi/180, 'DOWN')

            global distance
            # приближение
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 5:
                    if distance > 2:
                        distance *= 0.9
                    pygame.display.flip()
                    screen.fill((100, 100, 100))
                    renderFigure(screen)

                if event.button == 4:
                    if distance < 50:
                        distance *= 1.1
                    pygame.display.flip()
                    screen.fill((100, 100, 100))
                    renderFigure(screen)

    pygame.display.flip()

main()
