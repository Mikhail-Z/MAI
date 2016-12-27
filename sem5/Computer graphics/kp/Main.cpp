#include <iostream>
#include <Windows.h>
#include <stdio.h>
#include <stdarg.h>
#include <math.h>
#include <gl\GLU.h>
#include <glut.h>
#include <stdlib.h>
#include <cstdlib>
#include <math.h>
#include <fstream>
#include <string>
#include "Serialize.h"
#include "pugi_xml/pugixml.hpp"
#include "XML_Serialize.h"

using namespace std;

wchar_t *filename;
int arg_count = 1;

struct Float3
{
	float X = 0;
	float Y = 0;
	float Z = 0;
};

template<>
void Deserialize(const string& _key, Float3* _val, const pugi::xml_node& _node)
{
	auto lv_Node = _node.child(_key.c_str());
	_val->X = lv_Node.attribute("x").as_float();
	_val->Y = lv_Node.attribute("y").as_float();
	_val->Z = lv_Node.attribute("z").as_float();
}

template<>
void Serialize(const string& _key, Float3* _val, pugi::xml_node& _node)
{
	auto lv_Node = _node.append_child(_key.c_str());
	lv_Node.append_attribute("x") = _val->X;
	lv_Node.append_attribute("y") = _val->Y;
	lv_Node.append_attribute("z") = _val->Z;
}



class Transform : public Serializable < pugi::xml_node >
{
public:
	Float3 point1;
	Float3 point2;
	Float3 point3;
	Float3 point4;

private:
	serialize(point1);
	serialize(point2);
	serialize(point3);
	serialize(point4);
};

class TestClass : public Serializable<pugi::xml_node>
{

public:

	Transform Point;

private:
	serialize(Point);

};

float X_look, Y_look, Z_look, R_look;//повороты камеры
GLdouble objX, objY, objZ;  //координаты клика мыши
float FOldMouseX, FOldMouseY; //для сдвига координат мыши
float a, b, c = 0; //сдвиги камеры
float sc = 1; //масштаб
int n;  //степень аппроксимации
GLdouble matrix[13][13][3];  //матрица высот, размер должен быть на+1 больше чем степень апроксимации
GLdouble p[4][3]; //4 опорные точки
GLUquadricObj *quadObj;    //для отрисовки сфер
int pointNum = -1; //номер выбранной точки
int fillTyp = 1;  //тип отображения сеткой/закрашено
int curHeight = 600;
int curWidth = 800;
int btnNum = 0;

void SetupLighting()  //установка источника света
{
	GLfloat front_color[] = { 0, 1, 0, 1 };
	GLfloat back_color[] = { 0, 0, 1, 1 };
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
	glMaterialfv(GL_FRONT, GL_DIFFUSE, front_color);
	glMaterialfv(GL_BACK, GL_DIFFUSE, back_color);
	glLightModeli(GL_LIGHT_MODEL_TWO_SIDE, GL_TRUE);
	glEnable(GL_LIGHTING);
	glEnable(GL_LIGHT0);

	glEnable(GL_COLOR_MATERIAL);

}

GLvoid MyDisplay() {
	glClearColor(0, 0.6, 1, 0);
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
	glLoadIdentity();

	//установка закраски/каркаса
	if (fillTyp == 1) glPolygonMode(GL_FRONT_AND_BACK, GL_FILL);
	if (fillTyp == -1) glPolygonMode(GL_FRONT_AND_BACK, GL_LINE);

	a = -0.5*sc;
	b = -0.5*sc;
	c = 0;
	glTranslatef(0.0, 0, -9.0);
	glRotatef(X_look, 1.0f, 0.0f, 0.0f);
	glRotatef(Y_look, 0.0f, 0.0f, 1.0f);
	glRotatef(R_look, 0.0f, 1.0f, 0.0f);
	glTranslatef(a, 0.0, 0.0);
	glTranslatef(0.0, b, 0.0);
	glTranslatef(0.0, 0.0, c);
	glScaled(sc, sc, sc);
	SetupLighting();
	glColor3f(1, 1, 1);

	float d = 1.0 / n;
	for (int i = 0; i<n + 1; i++)      //рисуем сетку основу
		for (int j = 0; j<n + 1; j++){
			glBegin(GL_LINES);
			glVertex3f(i*d, 1, 0); glVertex3f(i*d, 0, 0);
			glVertex3f(0, i*d, 0); glVertex3f(1, i*d, 0);
			glEnd();
		}

	float  dx = 1.0 / n;
	float  dy = 1.0 / n;
	float  xx = 0;
	float  yy = 0;
	for (int i = 0; i<n + 1; i++) //расчитываем высоту в промежуточных точках, и заполняем координаты точек
		for (int j = 0; j<n + 1; j++){
			yy = dy*j;
			xx = dx*i;
			matrix[i][j][0] = xx;
			matrix[i][j][1] = yy;
			matrix[i][j][2] = p[0][2] * (1 - xx) *
				(1 - yy) + p[2][2] * (1 - yy)*xx + p[1][2] * (1 - xx)*yy + p[3][2] * xx * yy;
		}

	glEnable(GL_AUTO_NORMAL);
	glEnable(GL_NORMALIZE);
	for (int i = 0; i<n; i++)  //рисуем поверхность
		for (int j = 0; j<n; j++){
			glColor3f(0.5, 0.7, 0.1);
			float  dx = 1.0 / n;
			glNormal3f(0, 0, 1);

			float xx1, xx2, xx3, yy1, yy2, yy3, zz1, zz2, zz3;
			float x1, x2, x3, y1, y2, y3, z1, z2, z3;
			xx1 = (matrix[i][j][0]); yy1 = (matrix[i][j][1]); zz1 = (matrix[i][j][2]);
			xx2 = (matrix[i + 1][j][0]); yy2 = (matrix[i + 1][j][1]); zz2 = (matrix[i + 1][j][2]);
			xx3 = (matrix[i + 1][j + 1][0]); yy3 = (matrix[i + 1][j + 1][1]); zz3 = (matrix[i + 1][j + 1][2]);
			x1 = xx1 - xx3;
			y1 = yy1 - yy3;
			z1 = zz1 - zz3;   //рассчет нормалей
			x2 = xx2 - xx3;
			y2 = yy2 - yy3;
			z2 = zz2 - zz3;
			glNormal3f(y1*z2 - y2*z1, x2*z1 - x1*z2, x1*y2 - x2*y1);
			glBegin(GL_QUADS);
			glColor3f(matrix[i][j][2], 1 - matrix[i][j][2], 0);
			glVertex3f(matrix[i][j][0], matrix[i][j][1], matrix[i][j][2]);
			glVertex3f(matrix[i + 1][j][0], matrix[i + 1][j][1], matrix[i + 1][j][2]);
			glVertex3f(matrix[i + 1][j + 1][0], matrix[i + 1][j + 1][1], matrix[i + 1][j + 1][2]);
			glVertex3f(matrix[i][j + 1][0], matrix[i][j + 1][1], matrix[i][j + 1][2]);
			glEnd();
		}
	glColor3f(0, 1, 0);
	float r = 0.03;
	for (int i = 0; i<4; i++)  //рисуем 4 точки сферами
	{
		glPushMatrix(); glTranslatef(p[i][0], p[i][1], p[i][2]); gluSphere(quadObj, r, 10, 10); glPopMatrix();
	}

	glFlush();
}

GLvoid ShowFigure() {
	MyDisplay();
	glFlush();
}


bool InitGL() {
	glShadeModel(GL_SMOOTH);
	glClearColor(0.0f, 0.0f, 0.0f, 0.5f);
	glClearDepth(1.0f);
	glEnable(GL_DEPTH_TEST);
	glDepthFunc(GL_LEQUAL);
	glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST);
	SetupLighting();
	return TRUE;
}

GLvoid MyResize(GLint w, GLint h) {
	glViewport(0, 0, w, h);
	glMatrixMode(GL_PROJECTION);
	glLoadIdentity();
	gluPerspective(30, static_cast<double>(w) / static_cast<double>(h), 5, 200);
	glMatrixMode(GL_MODELVIEW);
	glLoadIdentity();
	curHeight = h;
	curWidth = w;
}

GLvoid MyRotation(int Key, int x, int y) {
	//обработка нажатий клавиатуры
	if (Key == GLUT_KEY_LEFT) Y_look = Y_look + 5;
	if (Key == GLUT_KEY_RIGHT) Y_look = Y_look - 5;
	if (Key == GLUT_KEY_UP) X_look = X_look - 5;
	if (Key == GLUT_KEY_DOWN) X_look = X_look + 5;
	glutPostRedisplay();
}

GLvoid MyScale(unsigned char Key, int x, int y) {
	if (Key == '+') sc = sc*1.1;
	if (Key == '-') sc = sc*0.9;
	if (Key == 's') {
		TestClass lv_Test;
		lv_Test.Point.point1.X = p[0][0];
		lv_Test.Point.point1.Y = p[0][1];
		lv_Test.Point.point1.Z = p[0][2];
		lv_Test.Point.point2.X = p[1][0];
		lv_Test.Point.point2.Y = p[1][1];
		lv_Test.Point.point2.Z = p[1][2];
		lv_Test.Point.point3.X = p[2][0];
		lv_Test.Point.point3.Y = p[2][1];
		lv_Test.Point.point3.Z = p[2][2];
		lv_Test.Point.point4.X = p[3][0];
		lv_Test.Point.point4.Y = p[3][1];
		lv_Test.Point.point4.Z = p[3][2];
		pugi::xml_document doc;
		auto lv_Node = doc.append_child("Serialization");
		lv_Test.Serialize(lv_Node);
		if (arg_count == 1) {
			doc.save_file(L"Test.xml");
		}
		else if (arg_count == 2) {
			if (doc.save_file(filename))
				cout << "yes!" << endl;
		}
	}
	glutPostRedisplay();
}

GLvoid MyReshape(int button, int state, int X, int Y) {
	if (button == GLUT_LEFT_BUTTON && state == GLUT_DOWN) {
		FOldMouseY = Y;
		FOldMouseX = X;

		btnNum = 1;

		GLint vport[4];  // получаем координаты мыши в 3д+++++
		GLdouble modl[16], proj[16];
		int glX = X;
		int glY = curHeight - 1 - Y;
		GLfloat depth;
		glGetIntegerv(GL_VIEWPORT, vport);
		glGetDoublev(GL_MODELVIEW_MATRIX, modl);
		glGetDoublev(GL_PROJECTION_MATRIX, proj);
		glReadPixels(glX, glY, 1, 1, GL_DEPTH_COMPONENT, GL_FLOAT, &depth);
		bool t = gluUnProject(glX, glY, depth, modl, proj, vport, &objX, &objY, &objZ);  //получаем координаты мыши в 3д-----

		if (t == 1)
			for (int i = 0; i < 4; i++){  //проверяем расстояние от клика мыши до точек
				GLdouble dist = (
					(objX - p[i][0])*(objX - p[i][0])
					+ (objY - p[i][1])*(objY - p[i][1])
					+ (objZ - p[i][2])*(objZ - p[i][2])
					);
				if (dist < 0.1*0.1)pointNum = i;
			}
	}
	if (button == GLUT_LEFT_BUTTON && state == GLUT_UP) {
		pointNum = -1;
		btnNum = 0;
		glutPostRedisplay();
	}
	if (button == GLUT_MIDDLE_BUTTON && state == GLUT_DOWN) {
		btnNum = 2;
	}
	if (button == GLUT_MIDDLE_BUTTON && state == GLUT_UP) {
		btnNum = 0;
	}
}

GLvoid MyReshapeContinue(int X, int Y) {
	if (btnNum == 1) {
		if (pointNum>-1)
		{
			p[pointNum][2] = p[pointNum][2] - (-FOldMouseY + Y) / 100;
			FOldMouseY = Y;
			FOldMouseX = X;
		};
		glutPostRedisplay();
	}
	else if (btnNum == 2) {
		Y_look = Y_look - (-FOldMouseX + X);
		X_look = X_look + (-FOldMouseY + Y);
		FOldMouseY = Y;
		FOldMouseX = X;
		glutPostRedisplay();
	}

}

GLvoid settings(int val) {
	switch (val) {
	case 13:
		fillTyp = 1;
		break;
	case 14:
		fillTyp = -1;
		break;
	default:
		n = val;
		break;
	}
	glutPostRedisplay();
}

bool isNumeric(char *str) {
	int n = strlen(str);
	if (n != 0) {
		int i = 0;
		if (str[0] == '-' || str[0] == '+')
			i++;
		for (; i < n - 1; i++) {
			if (!isdigit(str[i]) && str[i] != '.')
				return false;
		}
		return true;
	}
	else
		return false;
}

int main(int argc, char*argv[]){
	p[0][0] = 0; //задаем координаты 4 точек
	p[0][1] = 0;
	p[0][2] = 0;

	p[1][0] = 0;
	p[1][1] = 1;
	p[1][2] = -1;

	p[2][0] = 1;
	p[2][1] = 0;
	p[2][2] = 0.5;

	p[3][0] = 1;
	p[3][1] = 1;
	p[3][2] = 1;


	if (argc == 2) {
		arg_count = 2;
		size_t size = strlen(argv[1]);
		filename = new wchar_t[size+1];
		size_t out_size;
		MultiByteToWideChar(CP_ACP, 0, argv[1], -1, filename, size + 1);
		//mbstowcs_s(&out_size, filename, size, argv[1], size - 1);
		pugi::xml_document doc;
		if (doc.load_file(filename))
			cout << "yes" << endl;
		else cout << "no" << endl;
		auto lv_Node = doc.child("Serialization");
		TestClass lv_Test;
		lv_Test.Deserialize(lv_Node);

		p[0][0] = lv_Test.Point.point1.X;
		p[0][1] = lv_Test.Point.point1.Y;
		p[0][2] = lv_Test.Point.point1.Z;
		p[1][0] = lv_Test.Point.point2.X;
		p[1][1] = lv_Test.Point.point2.Y;
		p[1][2] = lv_Test.Point.point2.Z;
		p[2][0] = lv_Test.Point.point3.X;
		p[2][1] = lv_Test.Point.point3.Y;
		p[2][2] = lv_Test.Point.point3.Z;
		p[3][0] = lv_Test.Point.point4.X;
		p[3][1] = lv_Test.Point.point4.Y;
		p[3][2] = lv_Test.Point.point4.Z;

	}
	for (int i = 0; i < 4; i++) {
		cout << p[i][0] << " "<<p[i][1] <<" "<< p[i][2] << endl;
	}
	n = 12;     //степень апроксимации
	quadObj = gluNewQuadric();
	glutInit(&argc, argv);
	//glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB);
	glutInitWindowSize(800, 600);
	glutInitWindowPosition(0, 0);
	glutCreateWindow("zmk_kp");
	InitGL();
	glutReshapeFunc(MyResize);
	glutDisplayFunc(ShowFigure);
	glutKeyboardFunc(MyScale);
	glutSpecialFunc(MyRotation);
	glutMouseFunc(MyReshape);
	glutMotionFunc(MyReshapeContinue);
	int subMenu1 = glutCreateMenu(settings);
	glutAddMenuEntry("Filling", 13);
	glutAddMenuEntry("Frame", 14);

	int subMenu2 = glutCreateMenu(settings);
	glutAddMenuEntry("Approximation: 1", 1);
	glutAddMenuEntry("Approximation: 2", 2);
	glutAddMenuEntry("Approximation: 3", 3);
	glutAddMenuEntry("Approximation: 4", 4);
	glutAddMenuEntry("Approximation: 5", 5);
	glutAddMenuEntry("Approximation: 6", 6);
	glutAddMenuEntry("Approximation: 7", 7);
	glutAddMenuEntry("Approximation: 8", 8);
	glutAddMenuEntry("Approximation: 9", 9);
	glutAddMenuEntry("Approximation: 10", 10);
	glutAddMenuEntry("Approximation: 11", 11);
	glutAddMenuEntry("Approximation: 12", 12);

	int menu = glutCreateMenu(settings);
	glutAddSubMenu("Type of displaying", subMenu1);
	glutAddSubMenu("Approximaition power", subMenu2);

	glutAttachMenu(GLUT_RIGHT_BUTTON);
	glutMainLoop();
	
	
	return EXIT_SUCCESS;
}