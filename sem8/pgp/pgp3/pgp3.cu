#include "stdio.h" 
#include "stdlib.h"
#define MAX_NC 32
#define ERROR_HANDLING(call) {														\
    cudaError error = call;												\
    if(error != cudaSuccess) {											\
        fprintf(stderr, "ERROR: in file '%s' in line %i: %s.\n",	\
            __FILE__, __LINE__, cudaGetErrorString(error));				\
        exit(1);														\
    }																	\
} while (0)


typedef struct double24 {double x; double y; double z;} double24;

__device__
double24 rgb_sub(uchar4 *a, double24 *b) {
    double24 res = {a->x - b->x, a->y - b->y, a->z - b->z};
    return res;
}
__device__
double rgb_mul(double24 *a, double24 *b) {
    return a->x * b->x + a->y * b->y + a->z * b->z;
}

__constant__ double24 cavg_const[MAX_NC];
__constant__ int nc_const;

void copy_from_ram2dev_const(double24* cavg, int *nc) {
    ERROR_HANDLING(cudaMemcpyToSymbol(nc_const, nc, sizeof(int)));
    ERROR_HANDLING(cudaMemcpyToSymbol(cavg_const, cavg, (*nc)*sizeof(double24)));
}

__global__
void min_dist_method_kernel(uchar4* image, size_t width, size_t height) {
    size_t idx = threadIdx.x + blockIdx.x * blockDim.x;
    size_t idy = threadIdx.y + blockIdx.y * blockDim.y;
    size_t offsetx = blockDim.x * gridDim.x;
    size_t offsety = blockDim.y * gridDim.y;
    for (size_t x = idx; x < width; x+=offsetx) {
        for (size_t y = idy; y < height; y+=offsety) {
            uchar4* pixel = &image[x*height + y];
            
            int cur_max_class_idx = 0;
            double24 sub_res = rgb_sub(pixel, &cavg_const[cur_max_class_idx]);
            double cur_max_value = -rgb_mul(&sub_res, &sub_res);
            
            for (int i = 1; i < nc_const; i++) {
                double24 sub_res = rgb_sub(pixel, &cavg_const[i]);
                double res = - rgb_mul(&sub_res, &sub_res);
                if (res > cur_max_value) {
                    cur_max_value = res;
                    cur_max_class_idx = i;
                }
            }
            pixel->w  = cur_max_class_idx;
        }
    }
}

int main() {
    int width, height;
    char inputFilename[256];
    char outputFilename[256];
    scanf("%s", inputFilename);
    scanf("%s", outputFilename);
    FILE* file = fopen(inputFilename, "rb");

    fread(&width, sizeof(int), 1, file);
    fread(&height, sizeof(int), 1, file);
    uchar4* image = (uchar4*)malloc(sizeof(uchar4)*height*width);
    fread(image, sizeof(uchar4), width*height, file);
    fclose(file);

    int nc;
    scanf("%d", &nc);

    double24 cavg[MAX_NC];

    int np_i;
    for (int i = 0; i < nc; i++) {
    	scanf("%d", &np_i);
        double24 tmp_sum = {0., 0., 0.};
        int x, y;
    	for (int j = 0; j < np_i; j++) {
    		scanf("%d %d", &x, &y);
            tmp_sum.x += image[y*width+x].x;
            tmp_sum.y += image[y*width+x].y;
            tmp_sum.z += image[y*width+x].z;
    	}
        cavg[i].x = tmp_sum.x/np_i;
        cavg[i].y = tmp_sum.y/np_i;
        cavg[i].z = tmp_sum.z/np_i;
    }
    copy_from_ram2dev_const(cavg, &nc);	
    uchar4* dimage;
    ERROR_HANDLING(cudaMalloc((void**)&dimage, sizeof(uchar4)*width*height));
    ERROR_HANDLING(cudaMemcpy(dimage, image, sizeof(uchar4)*width*height, cudaMemcpyHostToDevice));
    min_dist_method_kernel<<<dim3(16, 16), dim3(16, 16)>>>(dimage, width, height);
    ERROR_HANDLING(cudaGetLastError());
    ERROR_HANDLING(cudaMemcpy(image, dimage, sizeof(uchar4)*width*height, cudaMemcpyDeviceToHost));
    ERROR_HANDLING(cudaFree(dimage));
    file = fopen(outputFilename, "wb");
    fwrite(&width, sizeof(int), 1, file);
    fwrite(&height, sizeof(int), 1, file);
    fwrite(image, sizeof(uchar4), width * height, file);
    fclose(file);
    free(image);
    return 0;
}
