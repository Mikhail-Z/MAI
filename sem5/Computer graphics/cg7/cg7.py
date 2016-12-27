import pylab as plt

import matplotlib

matplotlib.use('TkAgg')

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure

import numpy as np

import tkinter as tk
from tkinter import ttk
from tkinter import *

approximation = 100

Points = [[0, 0] for i in range(4)]

def CatmullRomSpline(P0, P1, P2, P3, nPoints=100):

  t = 0
  epsylon = 1 / nPoints
  old_x = P1[0]
  old_y = P1[1]

  points = []
  while t < 1:
      t += epsylon
      a = 0.5 * (-t * (1 - t) ** 2)
      b = 0.5 * (2 - 5 * t ** 2 + 3 * t ** 3)
      c = 0.5 * t * (1 + 4 * t - 3 * t ** 2)
      d = 0.5 * (-t ** 2 * (1 - t))
      x = a * P0[0] + b * P1[0] + c * P2[0] + d * P3[0]
      y = a * P0[1] + b * P1[1] + c * P2[1] + d * P3[1]
      points.append([old_x, old_y])
      points.append([x, y])
      old_x = x
      old_y = y

  return points

def CatmullRomChain(P):
  global  approximation

  sz = len(P)
  # Кривая состоит из массива точек
  C = []
  for i in range(sz-3):
    c = CatmullRomSpline(P[i], P[i+1], P[i+2], P[i+3], 2**approximation)
    C.extend(c)

  return C

class Application(tk.Tk):
    def __init__(self, *args, **kwargs):  # конструктор класса
        tk.Tk.__init__(self, *args, **kwargs)  # позиционные и именные аргументы
        title1 = self.title("Catmul Rom Spline")
        self.minsize(250, 250)
        print("made by zmk")
        row_num = 0
        self.label0 = tk.Label(self, text="Enter approximation (from 2 to 10)")
        self.label0.grid(row=row_num, columnspan=2)
        self.ent1 = tk.Entry(self)  # создание поля ввода
        self.ent1.grid(columnspan=2)
        row_num += 1
        self.ent1.bind('<Any-KeyRelease>', self.foo)  # связываю звполнение поля ввода с состоянием кнопки
        self.ent1.grid(row=row_num)
        row_num += 1
        self.label1 = tk.Label(self, text="Enter points:")
        self.label1.grid(row=row_num, columnspan=2)
        global Points
        #row_num += 1
        #tk.Label(self, text="").grid(row=row_num)
        row_num += 1
        self.label2 = tk.Label(self, text="x1=")
        self.label2.grid(row=row_num, column=0)
        self.ent2 = tk.Entry(self)  # создание поля ввода
        self.ent2.bind('<Any-KeyRelease>', self.foo)  # связываю звполнение поля ввода с состоянием кнопки
        self.ent2.grid(row=row_num, column=1)

        row_num += 1
        self.label3 = tk.Label(self, text="y1=")
        self.label3.grid(row=4, column=0)
        self.ent3 = tk.Entry(self)  # создание поля ввода
        self.ent3.bind('<Any-KeyRelease>', self.foo)  # связываю звполнение поля ввода с состоянием кнопки
        self.ent3.grid(row=4, column=1)

        row_num += 1
        tk.Label(self, text="").grid(row=row_num)
        row_num += 1
        self.label4 = tk.Label(self, text="x2=")
        self.label4.grid(row=row_num, column=0)
        self.ent4 = tk.Entry(self)  # создание поля ввода
        self.ent4.bind('<Any-KeyRelease>', self.foo)  # связываю звполнение поля ввода с состоянием кнопки
        self.ent4.grid(row=row_num, column=1)

        row_num += 1
        self.label5 = tk.Label(self, text="y2=")
        self.label5.grid(row=row_num, column=0)
        self.ent5 = tk.Entry(self, textvariable=Points[1][1])  # создание поля ввода
        self.ent5.bind('<Any-KeyRelease>', self.foo)  # связываю звполнение поля ввода с состоянием кнопки
        self.ent5.grid(row=row_num, column=1)

        row_num += 1
        tk.Label(self, text="").grid(row=row_num)
        row_num += 1
        self.label6 = tk.Label(self, text="x3=")
        self.label6.grid(row=row_num, column=0)
        self.ent6 = tk.Entry(self)  # создание поля ввода
        self.ent6.bind('<Any-KeyRelease>', self.foo)  # связываю звполнение поля ввода с состоянием кнопки
        self.ent6.grid(row=row_num, column=1)

        row_num += 1
        self.label7 = tk.Label(self, text="y3=")
        self.label7.grid(row=row_num, column=0)
        self.ent7 = tk.Entry(self)  # создание поля ввода
        self.ent7.bind('<Any-KeyRelease>', self.foo)  # связываю звполнение поля ввода с состоянием кнопки
        self.ent7.grid(row=row_num, column=1)

        row_num += 1
        tk.Label(self, text="").grid(row=row_num)
        row_num += 1
        self.label8 = tk.Label(self, text="x4=")
        self.label8.grid(row=row_num, column=0)
        self.ent8 = tk.Entry(self)  # создание поля ввода
        self.ent8.bind('<Any-KeyRelease>', self.foo)  # связываю звполнение поля ввода с состоянием кнопки
        self.ent8.grid(row=row_num, column=1)

        row_num += 1
        self.label9 = tk.Label(self, text="y4=")
        self.label9.grid(row=row_num, column=0)
        self.ent9 = tk.Entry(self)  # создание поля ввода
        self.ent9.bind('<Any-KeyRelease>', self.foo)  # связываю звполнение поля ввода с состоянием кнопки
        self.ent9.grid(row=row_num, column=1)

        row_num += 1
        self.btn = ttk.Button(self, text="Graph page", state='disabled', command=self.show)  # название Graph page,
        # состояние по умалчанию неактивное, при нажатии вызывается функция show
        self.btn.grid(row=row_num, columnspan=2)

    def foo(self, event):
        global approximation
        global Points
        tmp = self.ent1.get()
        if tmp >= "1" and len(tmp) != 0:
            approximation = int(tmp)
        else:
            approximation = 8

        point = []
        point.append(self.ent2.get())
        point.append(self.ent3.get())
        if len(point[0]) != 0 and len(point[1]) != 0:
            Points[0] = [int(point[0]), int(point[1])]
            self.ent2.winfo_viewable()
            point.clear()

        point.clear()
        point.append(self.ent4.get())
        point.append(self.ent5.get())
        if len(point[0]) != 0 and len(point[1]) != 0:
            Points[1] = [int(point[0]), int(point[1])]
            point.clear()

        point.clear()
        point.append(self.ent6.get())
        point.append(self.ent7.get())
        if len(point[0]) != 0 and len(point[1]) != 0:
            Points[2] = [int(point[0]), int(point[1])]
            point.clear()

        point.clear()
        point.append(self.ent8.get())
        point.append(self.ent9.get())
        if len(point[0]) != 0 and len(point[1]) != 0:
            Points[3] = [int(point[0]), int(point[1])]
            point.clear()

        if len(tmp) != 0:
            self.btn.config(state='enabled')

        point.clear()

    def show(self):
        self.btn.config(state='disabled')

        global Points
        # высчитываем сегмент кривой Кэтмула Рома по 4 точкам
        c = CatmullRomChain(Points)

        # Рисуем график по точкам
        x, y = zip(*c)
        plt.plot(x, y)

        # Plot the control points
        px, py = zip(*Points)
        plt.plot(px, py, 'or')

        plt.show()
        self.exit()

    def exit(self):
        self.destroy()

window = Application()
window.mainloop()