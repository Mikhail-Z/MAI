# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'nm1.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import random
from numpy import pi
import re
import numpy as np
from nm1 import *
import matplotlib.pyplot as plt


class DifferentialParabolicEquationNMSolution():
    def __init__(self, H=pi/2):
        self.h = None
        self.tay = None
        self.m = None
        self.n = None
        self.t = None
        self.x0 = 0
        self.xl = H
        self.a = 1
        self.cur_ti = None
        self.delta = None
        self.u = None


class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.plot_is_shown = False
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)



class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1024, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.shema_box = QtWidgets.QGroupBox(self.centralwidget)
        self.shema_box.setObjectName("shema_box")
        self.explicit_appr_flag = QtWidgets.QRadioButton(self.shema_box)
        self.explicit_appr_flag.setGeometry(QtCore.QRect(0, 20, 100, 20))
        self.explicit_appr_flag.setObjectName("explicit_appr_flag")
        self.implicit_app_flag = QtWidgets.QRadioButton(self.shema_box)
        self.implicit_app_flag.setGeometry(QtCore.QRect(0, 40, 100, 20))
        self.implicit_app_flag.setObjectName("implicit_app_flag")
        self.crank_Nicolson_flag = QtWidgets.QRadioButton(self.shema_box)
        self.crank_Nicolson_flag.setGeometry(QtCore.QRect(0, 60, 161, 20))
        self.crank_Nicolson_flag.setObjectName("crank_Nicolson_flag")
        self.horizontalLayout.addWidget(self.shema_box)
        self.approximation_box = QtWidgets.QGroupBox(self.centralwidget)
        self.approximation_box.setObjectName("approximation_box")
        self.two_points_one_appr = QtWidgets.QRadioButton(self.approximation_box)
        self.two_points_one_appr.setGeometry(QtCore.QRect(0, 20, 351, 20))
        self.two_points_one_appr.setObjectName("two_point_three_appr")
        self.three_points_two_appr = QtWidgets.QRadioButton(self.approximation_box)
        self.three_points_two_appr.setGeometry(QtCore.QRect(0, 40, 351, 20))
        self.three_points_two_appr.setObjectName("three_point_two_appr")
        self.two_points_two_appr = QtWidgets.QRadioButton(self.approximation_box)
        self.two_points_two_appr.setGeometry(QtCore.QRect(0, 60, 351, 20))
        self.two_points_two_appr.setObjectName("two_point_two_appr")
        self.horizontalLayout.addWidget(self.approximation_box)
        self.parameters_box = QtWidgets.QGroupBox(self.centralwidget)
        self.parameters_box.setObjectName("parameters_box")
        self.t_lineEdit = QtWidgets.QLineEdit(self.parameters_box)
        self.t_lineEdit.setGeometry(QtCore.QRect(40, 60, 61, 21))
        self.t_lineEdit.setObjectName("t_lineEdit")
        self.t_lbl = QtWidgets.QLabel(self.parameters_box)
        self.t_lbl.setGeometry(QtCore.QRect(10, 60, 21, 16))
        self.t_lbl.setObjectName("t_lbl")
        self.delta_lbl = QtWidgets.QLabel(self.parameters_box)
        self.delta_lbl.setGeometry(QtCore.QRect(120, 60, 51, 16))
        self.delta_lbl.setObjectName("delta_lbl")
        self.cur_ti_lbl = QtWidgets.QLabel(self.parameters_box)
        self.cur_ti_lbl.setGeometry(QtCore.QRect(230, 60, 40, 16))
        self.cur_ti_lbl.setObjectName("cur_ti_lbl")
        self.cur_ti_lbl.setText("cur ti:")

        self.cur_ti_lineEdit = QtWidgets.QLineEdit(self.parameters_box)
        self.cur_ti_lineEdit.setGeometry(QtCore.QRect(280, 60, 50, 21))
        self.cur_ti_lineEdit.setObjectName("cur_ti_lineEdit")
        self.cur_ti_lineEdit.setEnabled(False)

        self.n_lbl = QtWidgets.QLabel(self.parameters_box)
        self.n_lbl.setGeometry(QtCore.QRect(10, 30, 31, 16))
        self.n_lbl.setObjectName("n_lbl")
        self.n_lineEdit = QtWidgets.QLineEdit(self.parameters_box)
        self.n_lineEdit.setGeometry(QtCore.QRect(40, 30, 61, 22))
        self.n_lineEdit.setObjectName("n_lineEdit")
        self.m_lbl = QtWidgets.QLabel(self.parameters_box)
        self.m_lbl.setGeometry(QtCore.QRect(120, 30, 41, 16))
        self.m_lbl.setObjectName("m_lbl")
        self.m_lineEdit = QtWidgets.QLineEdit(self.parameters_box)
        self.m_lineEdit.setGeometry(QtCore.QRect(160, 30, 61, 22))
        self.m_lineEdit.setObjectName("m_lineEdit")
        self.m_lineEdit.setEnabled(False)
        self.delta_val_lbl = QtWidgets.QLabel(self.parameters_box)
        self.delta_val_lbl.setGeometry(QtCore.QRect(180, 60, 41, 16))
        self.delta_val_lbl.setText("")
        self.delta_val_lbl.setObjectName("delta_val_label")
        self.horizontalLayout.addWidget(self.parameters_box)
        self.horizontalLayout.setStretch(0, 3)
        self.horizontalLayout.setStretch(1, 6)
        self.horizontalLayout.setStretch(2, 6)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.OK_btn_Box = QtWidgets.QGroupBox(self.centralwidget)
        self.OK_btn_Box.setTitle("")
        self.OK_btn_Box.setObjectName("OK_btn_Box")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.OK_btn_Box)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.equation_lbl = QtWidgets.QLabel(self.OK_btn_Box)
        self.equation_lbl.setObjectName("equation_lbl")
        self.horizontalLayout_3.addWidget(self.equation_lbl)
        self.term1_lbl = QtWidgets.QLabel(self.OK_btn_Box)
        self.term1_lbl.setObjectName("term1_lbl")
        self.horizontalLayout_3.addWidget(self.term1_lbl)
        self.term2_lbl = QtWidgets.QLabel(self.OK_btn_Box)
        self.term2_lbl.setObjectName("term2_lbl")
        self.horizontalLayout_3.addWidget(self.term2_lbl)
        self.term3_lbl = QtWidgets.QLabel(self.OK_btn_Box)
        self.term3_lbl.setObjectName("term3_lbl")
        self.horizontalLayout_3.addWidget(self.term3_lbl)
        self.OK_btn = QtWidgets.QPushButton(self.OK_btn_Box)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.OK_btn.sizePolicy().hasHeightForWidth())
        self.OK_btn.setSizePolicy(sizePolicy)
        self.OK_btn.setObjectName("OK_btn")
        self.horizontalLayout_3.addWidget(self.OK_btn)
        self.verticalLayout.addWidget(self.OK_btn_Box)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setObjectName("widget")
        self.horizontalLayout_2.addWidget(self.widget)
        self.widget_2 = QtWidgets.QWidget(self.centralwidget)
        self.widget_2.setObjectName("widget_2")
        self.horizontalLayout_2.addWidget(self.widget_2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.verticalLayout.setStretch(0, 2)
        self.verticalLayout.setStretch(1, 1)
        self.verticalLayout.setStretch(2, 8)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 19))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.fig1 = PlotCanvas(width=5, height=4)
        self.fig2 = PlotCanvas(width=5, height=4)
        self.horizontalLayout_2.addWidget(self.fig1)
        self.horizontalLayout_2.addWidget(self.fig2)

        self.setupNMParams()
        self.m_lineEdit.editingFinished.connect(lambda: self.set_m())
        self.n_lineEdit.editingFinished.connect(lambda: self.set_n())
        self.t_lineEdit.editingFinished.connect(lambda: self.set_t())
        self.cur_ti_lineEdit.editingFinished.connect(lambda: self.set_cur_ti())
        self.OK_btn.released.connect(lambda: self.render_plot())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def setupNMParams(self):
        self.NMParams = DifferentialParabolicEquationNMSolution()

    def set_m(self):
        if re.match(r'^\d+$', self.m_lineEdit.text()):
            QtWidgets.QToolTip.hideText()
            if int(self.m_lineEdit.text()) < 10:
                QtWidgets.QToolTip.showText(self.m_lineEdit.mapToGlobal(QtCore.QPoint()),
                                            'too little m. It must be at least 10')
                print('-'*40)
                return

            self.NMParams.m = int(self.m_lineEdit.text())
            self.NMParams.tay = self.NMParams.t/(self.NMParams.m-1)
            self.delta_val_lbl.setText(str(round(self.NMParams.tay*self.NMParams.a**2/self.NMParams.h**2, 2)))
            self.cur_ti_lineEdit.setEnabled(True)
        else:
            QtWidgets.QToolTip.showText(self.m_lineEdit.mapToGlobal(QtCore.QPoint()),
                                        'm must be int')

    def set_t(self):
        if re.match(r'^-?\d+\.?\d*$', self.t_lineEdit.text()):
            QtWidgets.QToolTip.hideText()
            self.NMParams.t = float(self.t_lineEdit.text())
            if self.NMParams.m:
                self.NMParams.tay = self.NMParams.t / (self.NMParams.m - 1)
                self.delta_val_lbl.setText(
                    str(round(self.NMParams.tay * self.NMParams.a ** 2 / self.NMParams.h ** 2, 2)))
            self.m_lineEdit.setEnabled(True)
        else:
            QtWidgets.QToolTip.showText(self.m_lineEdit.mapToGlobal(QtCore.QPoint()),
                                        'right border of time must be float')

    def set_cur_ti(self):
        if re.match(r'^\d+$', self.cur_ti_lineEdit.text()):
            QtWidgets.QToolTip.hideText()
            if int(self.cur_ti_lineEdit.text()) < self.NMParams.m:
                self.NMParams.cur_ti = int(self.cur_ti_lineEdit.text())
                if self.fig1.plot_is_shown:
                    self.update_plot()
            else:
                QtWidgets.QToolTip.showText(self.cur_ti_lineEdit.mapToGlobal(QtCore.QPoint()),
                                            'cur_ti must be less than M')
                return
        else:
            QtWidgets.QToolTip.showText(self.cur_ti_lineEdit.mapToGlobal(QtCore.QPoint()),
                                        'cur_ti must be integer')

    def set_n(self):
        if re.match(r'^\d+$', self.n_lineEdit.text()):
            QtWidgets.QToolTip.hideText()
            if int(self.n_lineEdit.text()) < 10:
                QtWidgets.QToolTip.showText(self.m_lineEdit.mapToGlobal(QtCore.QPoint()),
                                            'too little n. It must be at least 10')
                return

            self.NMParams.n = int(self.n_lineEdit.text())
            self.NMParams.h = self.NMParams.xl/(self.NMParams.n-1)
            if self.NMParams.m:
                self.delta_val_lbl.setText(str(round(self.NMParams.tay*self.NMParams.a**2/self.NMParams.h**2, 2)))

        else:
            QtWidgets.QToolTip.showText(self.n_lineEdit.mapToGlobal(QtCore.QPoint()),
                                        'n must be int')

    def set_delta(self):
        self.NMParams.delta = self.NMParams.a**2*self.NMParams.tay/self.NMParams.h**2
        self.delta_val_lbl.setText(str(self.NMParams.delta))

    def init_u(self):
        m = self.NMParams.m
        n = self.NMParams.n
        h = self.NMParams.h
        tay = self.NMParams.tay
        x0 = self.NMParams.x0
        self.NMParams.u = np.empty([m, n])
        x = x0
        for i in range(n):
            self.NMParams.u[0][i] = term3(x)
            x += h
        time = 0
        for j in range(m):
            self.NMParams.u[j][0] = term1(time)
            time += tay

    def get_errors(self):
        errors = []
        for j in range(self.NMParams.m):
            target_v = np.array([f(self.NMParams.h*i, self.NMParams.tay*j) for i in range(self.NMParams.n)])
            errors.append(np.max(np.abs(target_v - self.NMParams.u[j])))
        return errors

    def update_plot(self):
        my_plot = self.NMParams.u[self.NMParams.cur_ti]
        target_plot = [f(self.NMParams.h * i, self.NMParams.tay * self.NMParams.cur_ti) for i in range(self.NMParams.n)]
        self.fig1.axes.clear()
        self.fig1.axes.plot(target_plot)
        self.fig1.axes.plot(my_plot)
        self.fig1.draw()

    def render_plot(self):
        if self.NMParams.n and self.NMParams.m and self.NMParams.cur_ti:
            self.init_u()

            if self.explicit_appr_flag.isChecked():
                if self.two_points_one_appr.isChecked():
                    expl_fin_dif_scheme_appr1(self.NMParams.u, self.NMParams.tay, self.NMParams.h,
                                              self.NMParams.m, self.NMParams.n)
                elif self.three_points_two_appr.isChecked():
                    expl_fin_dif_scheme_appr2(self.NMParams.u, self.NMParams.tay, self.NMParams.h,
                                              self.NMParams.m, self.NMParams.n)
                elif self.two_points_two_appr.isChecked():
                    expl_fin_dif_scheme_appr3(self.NMParams.u, self.NMParams.tay, self.NMParams.h,
                                              self.NMParams.m, self.NMParams.n)
                else:
                    QtWidgets.QToolTip.showText(self.OK_btn.mapToGlobal(QtCore.QPoint()), 'approximation was'
                                                                                          'not chosen')
                    return

            elif self.implicit_app_flag.isChecked():
                if self.two_points_one_appr.isChecked():
                    impl_fin_dif_scheme_appr1(self.NMParams.u, self.NMParams.tay, self.NMParams.h,
                                              self.NMParams.m, self.NMParams.n, self.NMParams.a)
                elif self.three_points_two_appr.isChecked():
                    impl_fin_dif_scheme_appr2(self.NMParams.u, self.NMParams.tay, self.NMParams.h,
                                              self.NMParams.m, self.NMParams.n, self.NMParams.a)
                elif self.two_points_two_appr.isChecked():
                    impl_fin_dif_scheme_appr3(self.NMParams.u, self.NMParams.tay, self.NMParams.h,
                                              self.NMParams.m, self.NMParams.n, self.NMParams.a)
                else:
                    QtWidgets.QToolTip.showText(self.OK_btn.mapToGlobal(QtCore.QPoint()), 'approximation was'
                                                                                          'not chosen')
                    return

            elif self.crank_Nicolson_flag.isChecked():
                if self.two_points_one_appr.isChecked():
                    expl_impl_fin_dif_scheme_appr1(self.NMParams.u, self.NMParams.tay, self.NMParams.h,
                                              self.NMParams.m, self.NMParams.n)
                elif self.three_points_two_appr.isChecked():
                    expl_impl_fin_dif_scheme_appr2(self.NMParams.u, self.NMParams.tay, self.NMParams.h,
                                              self.NMParams.m, self.NMParams.n, self.NMParams.a)
                elif self.two_points_two_appr.isChecked():
                    expl_impl_fin_dif_scheme_appr3(self.NMParams.u, self.NMParams.tay, self.NMParams.h,
                                              self.NMParams.m, self.NMParams.n, self.NMParams.a)
                else:
                    QtWidgets.QToolTip.showText(self.OK_btn.mapToGlobal(QtCore.QPoint()), 'approximation was'
                                                                                          'not chosen')
                    return
            else:
                QtWidgets.QToolTip.showText(self.OK_btn.mapToGlobal(QtCore.QPoint()), 'Scheme was not chosen.')
                return
        else:
            QtWidgets.QToolTip.showText(self.OK_btn.mapToGlobal(QtCore.QPoint()),
                                        'some parameters were not entered')
            return
        errors = self.get_errors()
        my_plot = self.NMParams.u[self.NMParams.cur_ti]
        target_plot = [f(self.NMParams.h*i, self.NMParams.tay*self.NMParams.cur_ti) for i in range(self.NMParams.n)]
        if self.fig1.plot_is_shown:
            self.fig1.axes.clear()
            self.fig2.axes.clear()
        else:
            self.fig1.plot_is_shown = True
        self.fig1.axes.plot([i*self.NMParams.h for i in range(self.NMParams.n)], target_plot)
        self.fig1.axes.plot([i*self.NMParams.h for i in range(self.NMParams.n)], my_plot)
        self.fig2.axes.plot([i*self.NMParams.tay for i in range(self.NMParams.m)], errors)
        self.fig1.draw()
        self.fig2.draw()


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.shema_box.setTitle(_translate("MainWindow", "Конечно-разностная схема"))
        self.explicit_appr_flag.setText(_translate("MainWindow", "Явная"))
        self.implicit_app_flag.setText(_translate("MainWindow", "Неявная"))
        self.crank_Nicolson_flag.setText(_translate("MainWindow", "Кранка-Николсона"))
        self.approximation_box.setTitle(_translate("MainWindow", "Способ аппроксимации"))
        self.two_points_one_appr.setText(_translate("MainWindow", "Двухточечная с первым порядком точности"))
        self.three_points_two_appr.setText(_translate("MainWindow", "Трёхточечная со вторым порядком точности"))
        self.two_points_two_appr.setText(_translate("MainWindow", "Двухточечная со вторым порядком точности"))
        self.parameters_box.setTitle(_translate("MainWindow", "Параметры сетки"))
        self.t_lbl.setText(_translate("MainWindow", "T:"))
        self.delta_lbl.setText(_translate("MainWindow", "delta:"))
        self.delta_val_lbl.setText(_translate("MainWindow", ""))
        self.n_lbl.setText(_translate("MainWindow", "n:"))
        self.m_lbl.setText(_translate("MainWindow", "m:"))
        self.equation_lbl.setText(_translate("MainWindow", "<html><head/><body><p><img src=\":/Prefix1/equation.png\"/></p></body></html>"))
        self.term1_lbl.setText(_translate("MainWindow", "<html><head/><body><p><img src=\":/Prefix2/term1.png\"/></p></body></html>"))
        self.term2_lbl.setText(_translate("MainWindow", "<html><head/><body><p><img src=\":/Prefix3/term2.png\"/></p></body></html>"))
        self.term3_lbl.setText(_translate("MainWindow", "<html><head/><body><p><img src=\":/Prefix4/term3.png\"/></p></body></html>"))
        self.OK_btn.setText(_translate("MainWindow", "OK"))


import nm1_rc
import nm2_rc
import nm3_rc
import nm4_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

