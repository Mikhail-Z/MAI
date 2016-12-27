# ��������� ��� ���������� ������������������� ����������� �������� �������������� ��������.
# ������ ������� �. �. �� �� 80-306�

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

import pygame
from pygame.locals import *

import numpy as np
import random
import math
from operator import itemgetter

import sys
angle_x, angle_y, angle_z = 0, 0, 0

# ��������� ��� ������� ������������ ������. ������ ������� �. �. �� �� 80-306�

verticies = [] # ������ ������
surfaces = [] # ������ ����������. ��� ������ ������� �������
colors = [] # ������ �������
appr_power = 0 # ������� �����������
n = 0 # ���-�� ������ ���������������
distance = 4 # ��������� �� �������
x = 1
y = 1 # ������ ������

class Point:
    def __init__(self, x=0, y=0, z=0):
        self.x, self.y, self.z = float(x), float(y), float(z) # ���������� �����

    # ������� ����������� ���� ��������� ������� �������� �� ������-�������, ����������� ��������� �����
    def rotate_x(self, angle):
        rad = angle * math.pi / 180
        cos_a = np.cos(rad)
        sin_a = np.sin(rad)
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
        cos_a = np.cos(rad)
        sin_a = np.sin(rad)
        x = self.x * cos_a - self.y * sin_a
        y = self.x * sin_a + self.y * cos_a
        return Point(x, y, self.z)

    def project(self, win_width, win_height, fov, viewer_distance):
        # factor using field of vision
        factor = fov / (viewer_distance + self.z)
        x = self.x * factor + win_width / 2
        y = -self.y * factor + win_height / 2
        # ��� ��� ��������� ��������������, �� z �� ������
        return Point(x, y, self.z)

def rotate(screen, param):
    global angle_x, angle_y, angle_z
    tVertices = []
    # ��� ������� ���������
    for vertex in verticies:
        rotation = vertex.rotate_x(angle_x).rotate_y(angle_y).rotate_z(angle_z)
        # �������� ���������� ����� � ������������ � ���������� ����������� (����� �� stackoverflow)
        projection = rotation.project(screen.get_width(), screen.get_height(), 256, distance)
        tVertices.append(projection)

    avgZ = []
    i = 0
    # ����������� ���������� ������
    for f in surfaces:
        if len(f) == 4:
            z = (tVertices[f[0]].z + tVertices[f[1]].z + tVertices[f[2]].z + tVertices[f[3]].z) / 4.0
        else:
            z = 0.0
            for j in range(n):
                z += tVertices[f[j]].z
            z = z/n

        # ��������� ���� <������, ���������� z ������>
        avgZ.append([i, z])
        i = i + 1

    # ��������� ������ ��� ����
    for zVal in sorted(avgZ, key=itemgetter(1), reverse=True):
        fIndex = zVal[0] # ����� ���������
        f = surfaces[fIndex] # ������ ������ � ���� ���������
        pointList = []
        if len(f) == 4:
            pointList = [(tVertices[f[0]].x, tVertices[f[0]].y), (tVertices[f[1]].x, tVertices[f[1]].y),
                         (tVertices[f[2]].x, tVertices[f[2]].y), (tVertices[f[3]].x, tVertices[f[3]].y)]
        else:
            i = 0
            while i < n:
                pointList.append((tVertices[f[i]].x, tVertices[f[i]].y))
                i += 1

        # ���������� ��������� �� ���� ��������
        pygame.draw.polygon(screen, colors[fIndex], pointList)
        pointList.clear()

    # ��������� ���������� ���� �������
    if (param == "UP"):
        angle_x += 2
    elif (param == "DOWN"):
        angle_x -= 2
    elif (param == "LEFT"):
        angle_y += 2
    elif (param == "RIGHT"):
        angle_y -= 2

    # �������� �����������
    pygame.display.flip()
    screen.fill((100, 100, 100))

# ���������� ������� rotate, �� ��� ��������� ����
def renderFigure(screen):
    global angleX, angleY, angleZ
    tVertices = []

    for vertex in verticies:
        rotation = vertex.rotate_x(angle_x).rotate_y(angle_y).rotate_z(angle_z)
        projection = rotation.project(screen.get_width(), screen.get_height(), 256, distance)
        tVertices.append(projection)
    avg_z = []
    i = 0
    for f in surfaces:
        if len(f) == 4:
            z = (tVertices[f[0]].z + tVertices[f[1]].z + tVertices[f[2]].z + tVertices[f[3]].z) / 4.0
        else:
            z = 0.0
            for j in range(n):
                z += tVertices[f[j]].z
            z = z/n

        avg_z.append([i, z])
        i = i + 1

    pointList = []
    for zVal in sorted(avg_z, key=itemgetter(1), reverse=True):
        fIndex = zVal[0]
        f = surfaces[fIndex]
        if len(f) == 4:
            pointList = [(tVertices[f[0]].x, tVertices[f[0]].y), (tVertices[f[1]].x, tVertices[f[1]].y),
                          (tVertices[f[2]].x, tVertices[f[2]].y), (tVertices[f[3]].x, tVertices[f[3]].y)]
        else:
            i = 0
            while i < n:
                pointList.append((tVertices[f[i]].x, tVertices[f[i]].y))
                i += 1

        pygame.draw.polygon(screen, colors[fIndex], pointList)
        pointList.clear()

    pygame.display.flip()


def main():
    pygame.init()
    win_width = 800
    win_height = 600
    global n
    r = 1/(2*np.sin(360/(2*n)))

    global appr_power
    screen = pygame.display.set_mode((win_width, win_height))
    screen.fill((100, 100, 100))
    for i in range((2**(appr_power)-1)*(2+n)):
        surfaces.append([])

    k = 0
    # ������������� ������� (������ ������ �������)
    for i in range(2**(appr_power)-1):
        a = 0
        for j in range(n):
            verticies.append(Point(r*np.cos(a*np.pi/180), -y + (2 * y / (2 ** (appr_power - 1)) * i), r*np.sin(a*np.pi/180)+i*x/2**(appr_power)-1))
            a += 180/n+180/n

        a = 0
        for j in range(n):
            verticies.append(Point(r * np.cos(a * np.pi / 180), -y + (2 * y / (2 ** (appr_power - 1)) * (i+1)), r * np.sin(a * np.pi / 180)+i*x/2**(appr_power)-1))
            a += 180/n+180/n

        # ������������� ��������� ��������
        for j in range(n):
            surfaces[k].append(j+2*i*n)
        colors.append([random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)])
        k += 1

        for j in range(n):
            surfaces[k].append(j+n + 2*i*n)
        colors.append([random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)])
        k += 1

        # ������������� ������� ��������� ��������
        for j in range(n):
            surfaces[k].append(j + 2*i*n)
            surfaces[k].append(j+n + 2*i*n)
            surfaces[k].append((j+1) % n + n + 2*i*n)
            surfaces[k].append((j+1) % n + 2*i*n)
            colors.append([random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)])
            k += 1


    renderFigure(screen)
    pygame.key.set_repeat(1,100)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    rotate(screen, 'LEFT')
                if event.key == pygame.K_RIGHT:
                    rotate(screen, 'RIGHT')
                if event.key == pygame.K_UP:
                    rotate(screen, 'UP')
                if event.key == pygame.K_DOWN:
                    rotate(screen, 'DOWN')

            global distance
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


class Application(tk.Tk):
    def __init__(self, *args, **kwargs):  # ����������� ������
        tk.Tk.__init__(self, *args, **kwargs)  # ����������� � ������� ���������
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

    def foo(self, event):
        global n, appr_power
        data1 = self.entry1.get()
        data2 = self.entry2.get()
        # ���� ���� ��������� �������� � ��� ���������, �� ������� ������ ��� ������� ��������
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
    if messagebox.askokcancel("Quit", "Do you want to quit?"): # ���� � ����������
        sys.exit(1)
        root.destroy()

app = Application() # ������ ���� ��� ����� ������
app.protocol("WM_DELETE_WINDOW", on_closing) # �������� ��� ��� ��������

app.mainloop()# ������ ����� ��������� ����
# main()