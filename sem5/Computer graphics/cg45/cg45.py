# ��������� ��� ���������� ������������������� ����������� �������� �������������� �������� �� OpenGL (8 �������).
# ������ ������� �. �. �� �� 80-306�

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

import sys
import numpy as np
import math

# ���� �������� ������������ ������� ���������
angle_x = 0.0
angle_y = 0.0
angle_z = 0.0

# ������� �����������
scaleFactor = -12.0

# ������� ������� ����� ������ ��� ������
alpha = 1
# ��� ��
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


# �����������
surfaces = [
]

# ������� � ������������
normals = []

x = 1
y = 1
# �������� ������������ ������
offsetx = 0
offsety = 0

# �������
verticies = [

]


# ������� �������� �� ������� �������
def rotationKeypress(key, x, y):
    global angle_x, angle_y, angle_z
    if key == GLUT_KEY_RIGHT:
        angle_y += 1  # ��������� ����������� ���� ��������
    elif key == GLUT_KEY_LEFT:
        angle_y -= 1
    elif key == GLUT_KEY_UP:
        angle_x += 1
    elif key == GLUT_KEY_DOWN:
        angle_x -= 1

    glutPostRedisplay()

# ��������� ��������� ���������� �����������
def initRendering():
    glEnable(GL_DEPTH_TEST)  # �� ������������ ��������� �����
    glEnable(GL_COLOR_MATERIAL) # ��������� ��������� �����
    glEnable(GL_LIGHTING)  # ��������� ��������� ������
    glEnable(GL_LIGHT0)  # ������� �������� �����
    glEnable(GL_LIGHT1)  # ������� �������� ����� ����� 2
    glEnable(GL_NORMALIZE)  # ���������� ������� ������������� ������������� ��� �����������
    glShadeModel(GL_SMOOTH)  # ��������� ������� ����
    # glEnable(GL_BLEND)
    # glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

# ������� ��� ���������� ������
def handleResize(w, h):
    glViewport(0, 0, w, h)  # ���������� ���� ������ ������ w � ������ h
    glMatrixMode(GL_PROJECTION)  # ������������� �� ������� ��������
    glLoadIdentity()  # ���������� ���� �������
    gluPerspective(45.0, w / h, 1.0, 200.0)  # ���������� ���� ������

# ������� ��� ��������� ������� � ���������, ������� �������� ����� ����� p1, p2, p3
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

# ������� ��� ��������� �����
def drawScene():
    # �������� ������� �������� ������ ������� ������ � ����� ��������� ������
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # ������������� �� ������� �������
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    global scale_flag
    # print(scale_flag)
    global scaleFactor
    global alpha
    print(alpha)
    # ����������
    glTranslatef(0.0, 0.0, scaleFactor)
    # glScalef(0.0, 0.0, scaleFactor)

    ambientColor = [0.2, 0.2, 0.2, 1.0]
    # ���������
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
            # ��� ����������� ��������� ����� ����������� ������� � �����������. ��� ������� ��� ���������
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

        # ������������� ������� ��������� ��������
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
    glutInit()  # ������������� ���������� gnut
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(400, 400)

    glutCreateWindow(b"zmk_lab45")
    initRendering()
    # ��������� ����������� ��� ���������� �� opengl ������� � ������
    glutDisplayFunc(drawScene)
    glutKeyboardFunc(handleKeypress)
    glutSpecialFunc(rotationKeypress)
    glutReshapeFunc(handleResize)

    # ������� ����
    glutMainLoop()


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
        tk.Label(self, text="press +/- for zooming")

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
    if messagebox.askokcancel("Quit", "Do you want to quit?"):  # ���� � ����������
        sys.exit(1)
        root.destroy()


app = Application()  # ������ ���� ��� ����� ������
app.protocol("WM_DELETE_WINDOW", on_closing)  # �������� ��� ��� ��������

app.mainloop()  # ������ ����� ��������� ����
# main()