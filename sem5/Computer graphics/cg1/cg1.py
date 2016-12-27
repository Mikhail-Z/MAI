import matplotlib

matplotlib.use('TkAgg')

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure

import numpy as np

import tkinter as tk
from tkinter import ttk



class Application(tk.Tk):
    def __init__(self, *args, **kwargs): #конструктор класса
        tk.Tk.__init__(self, *args, **kwargs)#позиционные и именные аргументы
        title1 = self.title("draw a graph y = ax^(3/2) (Zabelin)")

        print("made by zmk")
        self.label0 = tk.Label(self, text="y=ax^(3/2)")
        self.label0.pack()
        self.label1 = tk.Label(self, text="a=")
        self.label1.pack()
        self.ent1 = tk.Entry(self)#создание пол€ ввода
        self.ent1.bind('<Any-KeyRelease>', self.foo)#св€зываю звполнение пол€ ввода с состо€нием кнопки
        self.ent1.pack()

        self.label2 = tk.Label(self, text="b=")
        self.label2.pack()
        self.ent2 = tk.Entry(self)
        self.ent2.bind('<Any-KeyRelease>', self.foo)
        self.ent2.pack()#менеджер геометрии отрисовывает объект

        self.btn = ttk.Button(self, text="Graph page",state='disabled', command=self.show)#название Graph page,
        #состо€ние по умалчанию неактивное, при нажатии вызываетс€ функци€ show
        self.btn.pack()

    def foo(self, event):
        data1 = self.ent1.get()
        data2 = self.ent2.get()
        if len(data1) != 0 and len(data2) != 0:#если оба пол€ ввода не пусты
            self.btn.config(state='enabled')

    def show(self):
        self.btn.config(state='disabled') #делаю кнопку создани€ графика неактивной
        fig = Figure()#создаю главное окно
        fn = fig.add_subplot(111) #добавл€ю систему координат с положением по середине на все окно
        b = float(self.ent2.get())+1 #читаю данные из второго пол€ ввода (права€ граница)
        x = np.arange(0, b)
        a = float(self.ent1.get()) #читаю данные из первого пол€ ввода (коэф при x)
        y = a * x ** (3 / 2)
        line = fn.plot(x, y,  label = 'y = %dx^(3/2)' %a, color = 'green', linewidth=4, alpha = 0.5) #добавл€ю график
        xax = fn.xaxis  #ось x
        yax = fn.yaxis  #ось y

        xlabels = xax.get_ticklabels() #кортеж из делений на графике на оси X
        ylabels = yax.get_ticklabels()
        # Ћинии вспомогательной сетки (главные делени€) только по оси абсцисс
        xax.grid(True)
        st = 'Growth of sales'
        fn.set_title(st, size=20, color='green')
        fn.set_xlabel('ƒни', {'fontname': 'Arial'}, fontweight='light', fontsize=14, color='grey')
        fn.set_ylabel('ќбъем продаж', {'fontname': 'Arial'}, fontweight='light', fontsize=14, color='grey')

        for label in xlabels: #каждое деление красим в серый цвет и мен€ем размер шрифта
            # цвет подписи деленений оси OX
            label.set_color('grey')
            # размер шрифта подписей делений оси OX
            label.set_fontsize(14)

        for label in ylabels:
            label.set_color("grey")
            label.set_fontsize(16)

        fn.legend(loc='best', frameon=True) #легенда графика
        canvas = FigureCanvasTkAgg(fig, self)
        canvas.show()

        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas.get_tk_widget().pack()
        canvas._tkcanvas.pack()


window = Application()
window.mainloop() #запуск цикла обработки событий