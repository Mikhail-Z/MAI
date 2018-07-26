#include "cuda_runtime.h"
#include "device_launch_parameters.h"
#include <cstdio>
#include <cstdlib>


__global__ void kernelDeduct(double *a, double* b, double* c, size_t n) {
        size_t i = blockDim.x*blockIdx.x + threadIdx.x;
	size_t offset = gridDim.x*blockDim.x;
	for (; i < n; i+= offset){
		c[i] = a[i] - b[i];
	}
}


int main() {

        size_t n;

        scanf("%lu\n", &n);

        double *a = (double *)malloc(sizeof(double)*n);
        double *b = (double *)malloc(sizeof(double)*n);
        double *c = (double *)malloc(sizeof(double)*n);
	
	for (size_t i = 0; i < n; i++)
        	scanf("%lf", &a[i]);
	for (size_t i = 0; i < n; i++)
        	scanf("%lf", &b[i]);

        cudaError_t cudaStatus = cudaSetDevice(0);

        if (cudaStatus != cudaSuccess) {
	    printf("ERROR: %s\n", "cudaSetDevice check failed. You must have at least one Nvidia GPU!");
	    return 0;
	}
        double *va, *vb, *vc;


        cudaStatus = cudaMalloc((void**)&va, n*sizeof(double));
	if (cudaStatus != cudaSuccess) {
		printf("ERROR: %s\n", "Can't allocate video memory");
		return 0;
	}

        cudaStatus = cudaMalloc((void**)&vb, n*sizeof(double));
	if (cudaStatus != cudaSuccess) {
		printf("ERROR: %s\n", "Can't allocate video memory");
		return 0;
	}

        cudaStatus = cudaMalloc((void**)&vc, n*sizeof(double));
	if (cudaStatus != cudaSuccess) {
		printf("ERROR: %s\n", "Can't allocate video memory");
		return 0;
	}


        cudaStatus = cudaMemcpy(va, a, n*sizeof(double), cudaMemcpyHostToDevice);
	if (cudaStatus != cudaSuccess) {
		printf("ERROR: %s\n", "Can't copy from ram to videomemory");
		return 0;
	}

        cudaStatus = cudaMemcpy(vb, b, n*sizeof(double), cudaMemcpyHostToDevice);
	if (cudaStatus != cudaSuccess) {
		printf("ERROR: %s\n", "Can't copy from ram to videomemory");
		return 0;
	}

        kernelDeduct <<<16384, 512>>>(va, vb, vc, n);

	cudaStatus = cudaMemcpy(c, vc, n*sizeof(double), cudaMemcpyDeviceToHost);
	if (cudaStatus != cudaSuccess) {
		printf("ERROR: %s\n", "Can't copy from videomemory to ram");
		return 0;
	}

        cudaFree(va);
        cudaFree(vb);
        cudaFree(vc);

	for (size_t i = 0; i < n; i++)
            printf("%.10e ", c[i]);
	printf("\n");
        return 0;

}

