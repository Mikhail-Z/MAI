# программа для рендеринга аппроксимированного наколонного цилиндра многоугольными призмами на OpenGL (8 вариант).
# Сделал Забелин М. К. из гр 80-306Б

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

import sys
import numpy as np
import math

# углы поворота относительно мировых координат
angle_x = 0.0
angle_y = 0.0
angle_z = 0.0

# уровень приближения
scaleFactor = -12.0

# текущий уровень альфа канала для вершин
alpha = 1
# был ли
scale_flag = 0


def handleKeypress(key, x, y):
    global scaleFactor
    global scale_flag
    global alpha
    if key == b'-':
        scaleFactor *= 1.1
        scale_flag = 1
        glutPostRedisplay()
        if alpha <= 0.9:
            alpha += 0.1
    if key == b'+':
        scaleFactor *= 0.9
        scale_flag = 1
        glutPostRedisplay()
        if alpha >= 0.1:
            alpha -= 0.1


# поверхности
surfaces = [
]

# нормали к поверхностям
normals = []

x = 1
y = 1
# смещения относительно центра
offsetx = 0
offsety = 0

# вершины
verticies = [

]


# функция действия на нажатие клавишы
def rotationKeypress(key, x, y):
    global angle_x, angle_y, angle_z
    if key == GLUT_KEY_RIGHT:
        angle_y += 1  # изменение глобального угла поворота
    elif key == GLUT_KEY_LEFT:
        angle_y -= 1
    elif key == GLUT_KEY_UP:
        angle_x += 1
    elif key == GLUT_KEY_DOWN:
        angle_x -= 1

    glutPostRedisplay()

# установка начальных параметров отображения
def initRendering():
    glEnable(GL_DEPTH_TEST)  # не отрисовывать невидимые линии
    glEnable(GL_COLOR_MATERIAL) # разрешить изменение цвета
    glEnable(GL_LIGHTING)  # разрешить освещение фигуры
    glEnable(GL_LIGHT0)  # создать источник цвета
    glEnable(GL_LIGHT1)  # создать источник цвета номер 2
    glEnable(GL_NORMALIZE)  # нормальные векторы нормализуются автоматически при приближении
    glShadeModel(GL_SMOOTH)  # разрешить плавные тени
    # glEnable(GL_BLEND)
    # glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

# функция для увеличения фигуры
def handleResize(w, h):
    glViewport(0, 0, w, h)  # установить поле зрения ширины w и высоты h
    glMatrixMode(GL_PROJECTION)  # переключиться на матрицу прокциии
    glLoadIdentity()  # считывание этой матрицы
    gluPerspective(45.0, w / h, 1.0, 200.0)  # установить угол зрения

# функция для получения нормали к плоскости, которая проходит через точки p1, p2, p3
def getNormal(p1, p2, p3):
    v1 = [0, 0, 0]
    v2 = [0, 0, 0]
    v1[0] = p2[0] - p1[0]
    v2[0] = p3[0] - p1[0]

    v1[1] = p2[1] - p1[1]
    v2[1] = p3[1] - p1[1]

    v1[2] = p2[2] - p1[2]
    v2[2] = p3[2] - p1[2]

    n = [0, 0, 0]
    n[0] = v1[1] * v2[2] - v1[2] * v2[1]
    n[1] = v1[0] * v2[2] - v1[2] * v2[0]
    n[2] = v1[0] * v2[1] - v1[1] * v2[0]
    tmp0 = n[0]
    tmp1 = n[1]
    tmp2 = n[2]
    n[0] = n[0] / math.sqrt(tmp0 ** 2 + tmp1 ** 2 + tmp2 ** 2)
    n[1] = n[1] / math.sqrt(tmp0 ** 2 + tmp1 ** 2 + tmp2 ** 2)
    n[2] = n[2] / math.sqrt(tmp0 ** 2 + tmp1 ** 2 + tmp2 ** 2)
    return n

# функция для отрисовки сцены
def drawScene():
    # сбросить текущие значения буфера глубины вершин и увета эдементов фигуры
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # переключиться на видовую матрицу
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    global scale_flag
    # print(scale_flag)
    global scaleFactor
    global alpha
    print(alpha)
    # увеличение
    glTranslatef(0.0, 0.0, scaleFactor)
    # glScalef(0.0, 0.0, scaleFactor)

    ambientColor = [0.2, 0.2, 0.2, 1.0]
    # освещение
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, ambientColor)
    '''mat_specular = [1, 1, 1, 1]
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialf(GL_FRONT, GL_SHININESS, 128)'''
    lightColor0 = [0.5, 0.5, 0.5, 1.0]
    lightPos0 = [4.0, 0.0, 8.0, 1.0]
    glLightfv(GL_LIGHT0, GL_DIFFUSE, lightColor0)
    glLightfv(GL_LIGHT0, GL_POSITION, lightPos0)

    lightColor1 = [0.5, 0.2, 0.2, 1.0]
    lightPos1 = [-1.0, 0.5, 0.5, 0.0]
    glLightfv(GL_LIGHT1, GL_DIFFUSE, lightColor1)
    glLightfv(GL_LIGHT1, GL_POSITION, lightPos1)
    glRotatef(angle_x, 1, 0.0, 0.0)
    glRotatef(angle_y, 0.0, 1, 0.0)
    glColor3f(1.0, 1.0, 0.0)

    global verticies
    global surfaces
    k = 0
    for surface in surfaces:
        if len(surface) == 4:
            p = []
            glBegin(GL_QUADS)
            for i in surface:
                p.append(verticies[i])
            # для правильного освещения нужно высчитывать нормаль к поверхности. Все нормали уже посчитаны
            glNormal3f(normals[k][0], normals[k][1], normals[k][2])
            for i in surface:
                glVertex3f(verticies[i][0], verticies[i][1], verticies[i][2])
            glEnd()
        else:
            p = []
            glBegin(GL_POLYGON)
            for i in surface:
                p.append(verticies[i])

            glNormal3f(normals[k][0], normals[k][1], normals[k][2])
            print("-",normals[k])
            for i in surface:
                glVertex3f(verticies[i][0], verticies[i][1], verticies[i][2])
            glEnd()
        k += 1

    glutSwapBuffers()


appr_power = 0
n = 0


def main():
    global appr_power
    global n
    global normals
    for i in range((2 ** (appr_power) - 1) * (2 + n)):
        surfaces.append([])
    r = 1 / (2 * np.sin(360 / (2 * n)))
    k = 0
    for i in range(2 ** (appr_power) - 1):
        a = 0
        for j in range(n):
            print(i)
            print(r * np.sin(a * np.pi / 180))
            print(r * np.sin(a * np.pi / 180) + i * x / 2 ** (appr_power - 1))
            verticies.append([r * np.cos(a * np.pi / 180), -y + (2 * y / (2 ** (appr_power - 1)) * i),
                              r * np.sin(a * np.pi / 180) + i * x / 2 ** (appr_power - 1)])
            a += 180 / n + 180 / n

        a = 0
        for j in range(n):
            verticies.append([r * np.cos(a * np.pi / 180), -y + (2 * y / (2 ** (appr_power - 1)) * (i + 1)),
                              r * np.sin(a * np.pi / 180) + i * x / 2 ** (appr_power - 1)])
            a += 180 / n + 180 / n

        for j in range(n - 1, -1, -1):
            surfaces[k].append(j + 2 * i * n)
        p1 = verticies[surfaces[k][0]]
        p2 = verticies[surfaces[k][1]]
        p3 = verticies[surfaces[k][2]]
        print('++', p1,p2,p3,'++')
        normals.append(getNormal(p1, p2, p3))
        k += 1

        for j in range(n):
            surfaces[k].append(j + n + 2 * i * n)
        p1 = verticies[surfaces[k][0]]
        p2 = verticies[surfaces[k][1]]
        p3 = verticies[surfaces[k][2]]
        normals.append(getNormal(p1, p2, p3))
        k += 1
        print('++', p1,p2,p3,'++')

        # устанавливаем боковые плоскости трапеции
        for j in range(n):
            surfaces[k].append(j + 2 * i * n)
            surfaces[k].append(j + n + 2 * i * n)
            surfaces[k].append((j + 1) % n + n + 2 * i * n)
            surfaces[k].append((j + 1) % n + 2 * i * n)
            # colors.append([random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)])
            p1 = verticies[surfaces[k][0]]
            p2 = verticies[surfaces[k][1]]
            p3 = verticies[surfaces[k][2]]
            normals.append(getNormal(p1, p2, p3))
            k += 1
    glutInit()  # инициализация библиотеки gnut
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(400, 400)

    glutCreateWindow(b"zmk_lab45")
    initRendering()
    # связываем необходимые для приложения на opengl функции с нашими
    glutDisplayFunc(drawScene)
    glutKeyboardFunc(handleKeypress)
    glutSpecialFunc(rotationKeypress)
    glutReshapeFunc(handleResize)

    # главный цикл
    glutMainLoop()


class Application(tk.Tk):
    def __init__(self, *args, **kwargs):  # конструктор класса
        tk.Tk.__init__(self, *args, **kwargs)  # позиционные и именные аргументы
        tk.Label(self, text="made by zmk").pack()
        tk.Label(self, text="Enter approximation (1 to 8):").pack()
        self.entry1 = tk.Entry(self)
        self.entry1.bind("<Any-KeyRelease>", self.foo)
        self.entry1.pack()
        tk.Label(self, text="Enter number of sides (min 3):").pack()
        self.entry2 = tk.Entry(self)
        self.entry2.bind("<Any-KeyRelease>", self.foo)
        self.entry2.pack()
        self.btn = ttk.Button(self, text="Render", state='disabled', command=self.show)
        self.btn.pack()
        tk.Label(self, text="press +/- for zooming")

    def foo(self, event):
        global n, appr_power
        data1 = self.entry1.get()
        data2 = self.entry2.get()
        # если есть введенные значения и они допустимы, то сделать кнопку для рендера активной
        if len(data1) != 0 and len(data2) != 0:
            if int(data1) <= 8 and int(data1) > 0 and int(data2) > 2:
                self.btn.config(state="enabled")
                appr_power = int(data1)
                n = int(data2)

    def show(self):
        global appr_power
        appr_power = int(self.entry1.get())
        main()
        self.exit()

    def exit(self):
        self.destroy()


def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):  # окно с сообщением
        sys.exit(1)
        root.destroy()


app = Application()  # запуск окна для ввода данных
app.protocol("WM_DELETE_WINDOW", on_closing)  # действие при его закрытии

app.mainloop()  # запуск цикла обработки окна
# main()