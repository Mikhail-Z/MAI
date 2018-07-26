#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>
#include <GL/glew.h>
#include <GL/freeglut.h>
#include <cuda.h>
#include <cuda_runtime.h>
#include <cuda_gl_interop.h>
#include <thrust/sort.h>
#include <thrust/extrema.h>
#include <thrust/device_vector.h>
#include <curand.h>
#include <curand_kernel.h>
#include <thrust/execution_policy.h>

#define CSC(call) {                         \
    cudaError err = call;                       \
    if(err != cudaSuccess) {                        \
        fprintf(stderr, "CUDA error in file '%s' in line %i: %s.\n",    \
            __FILE__, __LINE__, cudaGetErrorString(err));       \
        exit(1);                            \
    }                                   \
} while (0)


const int width = 1024;
const int height = 768;
const int points_num = 600;

float a1 = 0.1;
float a2 = 0.3;
int seed = 0;

const float dt = 0.02;
float inertion = 0.8;
const float pointRadius = 0.3;

const float fminPointRadius = 0.5;
float xCenter = 0.0, yCenter = 0.0, xScale = 100.0, yScale = xScale * height / width, minFvalue = 0;

float2 *dev_points;
float2 *dev_velocity, *dev_localBest;
float *dev_Fvalue;
float* dev_dist;
float err;
GLuint vbo;

__constant__ float dev_xCenter, dev_yCenter, dev_xScale, dev_yScale, dev_minFvalue, dev_maxFvalue;
__constant__ float2 dev_globalBest;

__constant__ int dev_seed;


__device__ __host__
float Rozenbrock(float x, float y) {
    return (1 - x) * (1 - x) + 100 * (y - x * x) * (y - x * x);
}

__global__
void get_dist_to_fmin_pos(float2* points, int n, float* dists) {
    int idx = blockIdx.x*blockDim.x+threadIdx.x;
    int offset = gridDim.x*blockDim.x;
    for (int i = idx; i < n; i+=offset) {
        dists[i] = sqrtf(points[i].x*points[i].x + points[i].y*points[i].y);
    }
}

float get_mean_dist_to_fmin_pos() {
    get_dist_to_fmin_pos<<<32, 32>>>(dev_points, points_num, dev_dist);
    float mean_dist_to_fmin_pos = thrust::reduce(thrust::device, dev_dist, dev_dist + points_num)/points_num;
    CSC(cudaGetLastError());
    return mean_dist_to_fmin_pos;
}


__device__ __host__
float Rozenbrock(float2 p) {
    return Rozenbrock(p.x, p.y);
}

struct cmp {
    __device__ bool operator()(float2 p1, float2 p2) {
        return Rozenbrock(p1) < Rozenbrock(p2);
    }
};

__device__ float2 operator+(float2 p1, float2 p2) {
return make_float2(p1.x + p2.x, p1.y + p2.y);
}

__device__ float2 transformCoordToPixel(float x, float y) {
    int col = ((x-dev_xCenter)/dev_xScale+1.0)*(width-1)/2;
    int row = ((y-dev_yCenter)/dev_yScale+1.0)*(height-1)/2;
    return make_float2(col, row);
}
__device__ float2 transformPixelToCoord(int row, int col) {
    float x = (float(2 * col)/(width - 1) - 1.0)*dev_xScale+dev_xCenter;
    float y = (float(2 * row)/(height - 1) - 1.0)*dev_yScale+dev_yCenter;
    return make_float2(x, y);
}

__global__ void calculateF(float *f_val) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    int idy = blockIdx.y * blockDim.y + threadIdx.y;
    int offsetx = blockDim.x * gridDim.x;
    int offsety = blockDim.y * gridDim.y;
    int i, j;
    for (i = idx; i < width; i += offsetx) {
        for (j = idy; j < height; j += offsety) {
	    float2 coord = transformPixelToCoord(j, i);
            float f = Rozenbrock(coord);
            f_val[j * width + i] = f;
        }
    }
}

__host__ __device__
void print_array(float2* a, int n) {
    for (int i = 0; i < n; i++)
        printf("%.3f %.3f\n", a[i].x, a[i].y);
}

__global__ void updateCoord(float2* points, float2* v, int n) {
    int idx = blockIdx.x*blockDim.x + threadIdx.x;
    int offset = blockDim.x*gridDim.x;
    for (int i = idx; i < n; i += offset) {
        points[i].x += v[i].x*dt;
        points[i].y += v[i].y*dt;
    }
}


__global__ void drawPoints(uchar4* data, float2* points, int n) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    int offset = gridDim.x * blockDim.x;
    for (int i = idx; i < n; i += offset) {
        float2 _left_top_pixel = transformCoordToPixel(points[i].x-pointRadius, points[i].y-pointRadius);
        float2 _right_bottom_pixel = transformCoordToPixel(points[i].x+pointRadius, points[i].y+pointRadius);
        int2 right_bottom_pixel = make_int2(int(_right_bottom_pixel.x+0.5), int(_right_bottom_pixel.y+0.5));
        int2 left_top_pixel = make_int2(int(_left_top_pixel.x+0.5), int(_left_top_pixel.y+0.5));

        if (right_bottom_pixel.x - left_top_pixel.x == 0)
            right_bottom_pixel.x += 1;
        if (right_bottom_pixel.y - left_top_pixel.y == 0)
            right_bottom_pixel.y += 1;
        for (int i = max(0, left_top_pixel.x); i < min(width, right_bottom_pixel.x); i++) {
            for (int j = max(0,left_top_pixel.y); j < min(height, right_bottom_pixel.y); j++) {
                data[j * width + i] = make_uchar4(0, 0, 0, 255);
            }
        }
    }

    float2 _left_top_pixel = transformCoordToPixel(dev_globalBest.x-fminPointRadius, dev_globalBest.y-fminPointRadius);
    float2 _right_bottom_pixel = transformCoordToPixel(dev_globalBest.x+fminPointRadius, dev_globalBest.y+fminPointRadius);
    int2 right_bottom_pixel = make_int2(int(_right_bottom_pixel.x+0.5), int(_right_bottom_pixel.y+0.5));
    int2 left_top_pixel = make_int2(int(_left_top_pixel.x+0.5), int(_left_top_pixel.y+0.5));

    for (int i = max(0, left_top_pixel.x); i < min(width, right_bottom_pixel.x); i++) {
        for (int j = max(0,left_top_pixel.y); j < min(height, right_bottom_pixel.y); j++) {
            data[j * width + i] = make_uchar4(255, 0, 0, 255);
        }
    }
}


__global__ void drawBackground(uchar4* data, float* f_val) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    int idy = blockIdx.y * blockDim.y + threadIdx.y;
    int offsetx = blockDim.x * gridDim.x;
    int offsety = blockDim.y * gridDim.y;
    int i, j;
    for (i = idx; i < width; i += offsetx) {
        for (j = idy; j < height; j += offsety) {
            float f = ((f_val[j * width + i] - dev_minFvalue) / (dev_maxFvalue - dev_minFvalue));
            data[j * width + i] = make_uchar4(int(f * 255),  int((1-f) * 255), 0, 255);
        }
    }
}


__global__ void updateVelocity(float2 *points, float2 *v, float2 *localBest, int n, float inertion, float a1, float a2) {
    int idx = blockIdx.x*blockDim.x + threadIdx.x;
    int offset = blockDim.x*gridDim.x;

    for (int i = idx; i < n; i += offset) {
        float2 cur_force = make_float2(0, 0);
        for (int j = 0; j < n; j++) {
            if (j != i) {
                float x_dist = points[i].x - points[j].x;
                float y_dist = points[i].y - points[j].y;

                float g = sqrtf(x_dist*x_dist + y_dist*y_dist);
                cur_force.x += x_dist/powf(g, 4);
                cur_force.y += y_dist/powf(g, 4);
            }
        }
        curandState_t state;
        int MAX = 1000000;
        int seed = dev_seed;
        curand_init(seed, idx, 0, &state);
        float r1 = curand(&state) % MAX/float(MAX);
        float r2 = curand(&state) % MAX/float(MAX);
        v[i].x = v[i].x*inertion + (a1*r1*(dev_globalBest.x - points[i].x) + a2*r2*(localBest[i].x - points[i].x)+cur_force.x)*dt;
        r1 = curand(&state) % MAX/float(MAX);
        r2 = curand(&state) % MAX/float(MAX);
        v[i].y = v[i].y*inertion + (a1*r1*(dev_globalBest.y - points[i].y) + a2*r2*(localBest[i].y - points[i].y)+cur_force.y)*dt;
    }
}



void updateFMinMax() {
    thrust::device_ptr<float> dev_ptr = thrust::device_pointer_cast(dev_Fvalue);
    float Fmin = thrust::min_element(dev_ptr, dev_ptr + width * height)[0];
    float Fmax = thrust::max_element(dev_ptr, dev_ptr + width * height)[0];
    CSC(cudaMemcpyToSymbol(dev_minFvalue, &Fmin, sizeof(float)));
    CSC(cudaMemcpyToSymbol(dev_maxFvalue, &Fmax, sizeof(float)));
}

void updateCenter(float2* dev_points) {
    float2 sum = thrust::reduce(thrust::device, dev_points, dev_points + points_num, make_float2(0, 0), thrust::plus<float2>());
    CSC(cudaGetLastError());

    float avg_points_coord_influence_coef = 0.01;
    xCenter = xCenter + (sum.x / points_num - xCenter)*avg_points_coord_influence_coef;
    yCenter = yCenter + (sum.y / points_num - yCenter)*avg_points_coord_influence_coef;

    CSC(cudaMemcpyToSymbol(dev_xCenter, &xCenter, sizeof(float)));
    CSC(cudaMemcpyToSymbol(dev_yCenter, &yCenter, sizeof(float)));
}


__global__ void updateLocalMin(float2* points, float2* loc, int n) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    int offset = gridDim.x * blockDim.x;
    for (int i = idx; i < n; i += offset) {
        if (Rozenbrock(points[i]) < Rozenbrock(loc[i])) {
            loc[i].x = points[i].x;
            loc[i].y = points[i].y;
        }
    }
}

void updateGlobalMin(float2* localBest) {
    thrust::device_ptr<float2> arr_ptr = thrust::device_pointer_cast(localBest);

    thrust::device_ptr<float2> min_dptr = thrust::min_element(thrust::device, arr_ptr, arr_ptr + points_num, cmp());

    float2* min_ptr = thrust::raw_pointer_cast(min_dptr);
    CSC(cudaMemcpyToSymbol(dev_globalBest, min_ptr, sizeof(float2)));
}

void drawPicture(uchar4* dev_data) {
    drawBackground<<<dim3(32, 32), dim3(32, 32)>>>(dev_data, dev_Fvalue);
    CSC(cudaGetLastError());
    drawPoints<<<32, 32>>>(dev_data, dev_points, points_num);
    CSC(cudaGetLastError()); 
}

struct cudaGraphicsResource *res;


void update() {
    static float fps;
    static bool is_new_frame_counter = true;
    static int start;

    if (is_new_frame_counter) {
        start = clock();
        is_new_frame_counter = false;
    }
    uchar4* dev_data;
    size_t size;
    CSC(cudaGraphicsMapResources(1, &res, 0));
    CSC(cudaGraphicsResourceGetMappedPointer((void**)&dev_data, &size, res));

    updateGlobalMin(dev_localBest);
    updateVelocity<<<32, 32>>>(dev_points, dev_velocity, dev_localBest, points_num, inertion, a1, a2);
    updateCoord<<<32, 32>>>(dev_points, dev_velocity, points_num);
    updateCenter(dev_points);

    updateLocalMin<<<32, 32>>>(dev_points, dev_localBest, points_num);

    calculateF <<<dim3(32,32), dim3(32, 32)>>>(dev_Fvalue);
    updateFMinMax();
	
    drawPicture(dev_data);

    CSC(cudaGraphicsUnmapResources(1, &res, 0));
    glutPostRedisplay();

    int finish = clock();
    if ((float)(finish - start)/CLOCKS_PER_SEC >= 1.0) {
        err = get_mean_dist_to_fmin_pos();
        printf("FPS: %.3f\n", fps);
        printf("Error (mean distination to fmin position): %.3f\n", err);
        is_new_frame_counter = true;
        fps = 0;
    }
    else
        fps++;
}

void display() {
    glClearColor(0.0, 0.0, 0.0, 1.0);
    glClear(GL_COLOR_BUFFER_BIT);
    glDrawPixels(width, height, GL_RGBA, GL_UNSIGNED_BYTE, 0);
    glutSwapBuffers();
}

void special_keys(int key, int x, int y) {
    float val = 1;
    if (key == GLUT_KEY_LEFT) {
        xCenter -= val;
    }
    else if (key == GLUT_KEY_RIGHT) {
        xCenter += val;
    }
    else if (key == GLUT_KEY_UP) {
        yCenter += val;
    }
    else if (key == GLUT_KEY_DOWN) {
        yCenter -= val;
    }

    CSC(cudaMemcpyToSymbol(dev_xCenter, &xCenter, sizeof(float)));
    CSC(cudaMemcpyToSymbol(dev_yCenter, &yCenter, sizeof(float)));
}

void keys(unsigned char key, int x, int y) {
    if (key == '-') {
        xScale *= 1.1;
        yScale = xScale * height / width;
        CSC(cudaMemcpyToSymbol(dev_yScale, &yScale, sizeof(float)));
        CSC(cudaMemcpyToSymbol(dev_xScale, &xScale, sizeof(float)));
    } else if (key == '+') {
        xScale /= 1.1;
        yScale = xScale * height / width;
        CSC(cudaMemcpyToSymbol(dev_yScale, &yScale, sizeof(float)));
        CSC(cudaMemcpyToSymbol(dev_xScale, &xScale, sizeof(float)));
    }
    if (key == 'q') {
        CSC(cudaGraphicsUnregisterResource(res));
        glBindBuffer(1, vbo);
        glDeleteBuffers(1, &vbo);
        exit(0);
    }
}

void print_wrong_args_msg() {
    printf("Wrong arguments. They should be in this order: [-w] [-a1 -a2]\n");
    exit(0);
}

int main(int argc, char** argv) {
    srand(time(NULL));
    if (argc == 7) {
        if (strcmp(argv[1], "-w") == 0 && strcmp(argv[3], "-a1") == 0 && strcmp(argv[5], "-a2") == 0) {
            inertion = atof(argv[2]);
            a1 = atof(argv[4]);
            a2 = atof(argv[6]);
        } else
            print_wrong_args_msg();
    } else if (argc == 5) {
        if (strcmp(argv[1], "-a1") == 0 && strcmp(argv[3], "-a2") == 0) {

            a1 = atof(argv[2]);
            a2 = atof(argv[4]);
        } else
            print_wrong_args_msg();
    } else if (argc == 3) {
        if (strcmp(argv[1], "-w") == 0) {
            inertion = atof(argv[2]);
        } else
            print_wrong_args_msg();
    } else if (argc != 1)
        print_wrong_args_msg();

    CSC(cudaMalloc(&dev_points, points_num * sizeof(float2)));
    CSC(cudaMalloc(&dev_Fvalue, width * height * sizeof(float)));
    CSC(cudaMalloc(&dev_localBest, points_num * sizeof(float2)));
    CSC(cudaMalloc(&dev_dist, points_num * sizeof(float)));

    CSC(cudaMemcpyToSymbol(dev_xScale, &xScale, sizeof(float)));
    CSC(cudaMemcpyToSymbol(dev_yScale, &yScale, sizeof(float)));
    CSC(cudaMemcpyToSymbol(dev_xCenter, &xCenter, sizeof(float)));
    CSC(cudaMemcpyToSymbol(dev_yCenter, &yCenter, sizeof(float)));
    CSC(cudaMemcpyToSymbol(dev_minFvalue, &minFvalue, sizeof(float)));
    CSC(cudaMemcpyToSymbol(dev_seed, &seed, sizeof(int)));


    float2* temp = (float2*)malloc(points_num * sizeof(float2));
    for (int i = 0; i < points_num; i++) {
        temp[i].x = xScale * (2 * (rand() / float(RAND_MAX)) - 1) + xCenter;
        temp[i].y = yScale * (2 * (rand() / float(RAND_MAX)) - 1) + yCenter;
    }
    CSC(cudaMemcpy(dev_points, temp, points_num * sizeof(float2), cudaMemcpyHostToDevice));
    CSC(cudaMemcpy(dev_localBest, temp, points_num * sizeof(float2), cudaMemcpyHostToDevice));

    CSC(cudaMalloc(&dev_velocity, points_num * sizeof(float2)));
    for (int i = 0; i < points_num; i++) {
        temp[i].x = 10*xScale * (2 * (rand() / float(RAND_MAX)) - 1);
        temp[i].y = 10*xScale * (2 * (rand() / float(RAND_MAX)) - 1);
    }
    CSC(cudaMemcpy(dev_velocity, temp, points_num * sizeof(float2), cudaMemcpyHostToDevice));
    free(temp);

    glutInit(&argc, argv);
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA);
    glutInitWindowSize(width, height);
    glutCreateWindow("Zabelin KP");

    glutIdleFunc(update);
    glutDisplayFunc(display);
    glutKeyboardFunc(keys);
    glutSpecialFunc(special_keys);

    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    gluOrtho2D(0.0, (GLfloat) width, 0.0, (GLfloat) height);

    glewInit();

    GLuint vbo;
    glGenBuffers(1, &vbo);
    glBindBuffer(GL_PIXEL_UNPACK_BUFFER_ARB, vbo);
    glBufferData(GL_PIXEL_UNPACK_BUFFER_ARB, width * height * sizeof(uchar4), NULL, GL_DYNAMIC_DRAW);

    CSC(cudaGraphicsGLRegisterBuffer(&res, vbo, cudaGraphicsMapFlagsWriteDiscard));

    glutMainLoop();

    CSC(cudaGraphicsUnregisterResource(res));

    glBindBuffer(1, vbo);
    glDeleteBuffers(1, &vbo);
    return 0;
}
