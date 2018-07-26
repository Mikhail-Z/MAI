#include "stdlib.h"
#include "stdio.h"
#include <thrust/extrema.h>
#include <thrust/execution_policy.h>
#include <thrust/device_ptr.h>
#include "math.h"
#define BLOCK_SIZE 32

__global__
void swap_cols_kernel(double *a, int col1_idx, int col2_idx, int n) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    int offset = gridDim.x * blockDim.x;
    for (int row = idx; row < n; row+=offset) {
        double tmp = a[n*idx+col1_idx];
        a[n*idx+col1_idx] = a[n*idx+col2_idx];
        a[n*idx+col2_idx] = tmp;
    }
}

__global__
void coef_mul_and_sub_kernel(double *a, int fst_col_idx, int fst_row_idx, double *coefs, int n) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    int idy = blockIdx.y * blockDim.y + threadIdx.y;
    int offset_x = gridDim.x * blockDim.x;
    int offset_y = gridDim.y * blockDim.y;
    for (int i = fst_col_idx + idx; i < n; i+=offset_x) {
        for (int j = fst_row_idx+idy; j < n; j+=offset_y) {
            int diag_elem_idx = n*j+fst_col_idx-1;
            a[n*j + i] -=coefs[i]*a[diag_elem_idx];
        }

    }
}

struct compare_abs_value
{
    __host__ __device__
    bool operator()(double a, double b) {
        return (a<0? -a:a) < ( b<0? -b:b);
    }

};


void print_matrix(double *a, int n) {
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++)
            printf("%.10e ", a[j*n+i]);
        printf("\n");
    }
}

__global__
void set_cur_row_elements_kernel(double* a, double* coefs, int n, int row, int fst_col_idx) {
    int idx = blockDim.x*blockIdx.x + threadIdx.x;
    int offset = blockDim.x*gridDim.x;
    for (int col = idx+fst_col_idx; col < n; col+=offset) {
        coefs[col] = a[n*row+col]/a[n*row+fst_col_idx-1];
        a[n*row+col] = coefs[col];
    }

}


int main() {
    int n;
    scanf("%d", &n);
    double* a = (double*)malloc(sizeof(double)*n*n);
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++)
            scanf("%lf", &a[j*n+i]);
    }
    int size = sizeof(double)*n*n;
    double* d_a;
    cudaMalloc(&d_a, size);
    cudaMemcpy(d_a, a, size, cudaMemcpyHostToDevice);
    int* swap_vector = (int*)malloc(sizeof(int)*n);
    double *d_coefs;
    double *coefs = (double*)malloc(sizeof(double)*n);
    cudaMalloc(&d_coefs, n*sizeof(double));
    for (int row = 0; row < n-1; row++) {
        thrust::device_ptr<double> d_ptr = thrust::device_pointer_cast(&d_a[row*n+row]);

        thrust::device_ptr<double> d_row_begin_ptr = thrust::device_pointer_cast(&d_a[row*n]);
        thrust::device_ptr<double> max_elem_ptr = thrust::max_element(d_ptr, d_row_begin_ptr + n, compare_abs_value());
        int max_elem_idx = max_elem_ptr - d_row_begin_ptr;

        swap_vector[row] = max_elem_idx;

        swap_cols_kernel<<<(n+BLOCK_SIZE-1)/BLOCK_SIZE, BLOCK_SIZE>>>(d_a, row, max_elem_idx, n);

        set_cur_row_elements_kernel<<<((n-row-1)+BLOCK_SIZE-1)/BLOCK_SIZE, BLOCK_SIZE>>>(d_a, d_coefs, n, row, row+1);
        cudaMemcpy(coefs, d_coefs, sizeof(double)*n, cudaMemcpyDeviceToHost);


        dim3 dimGrid = dim3(((n-row-1)+BLOCK_SIZE-1)/BLOCK_SIZE, ((n-row-1)+BLOCK_SIZE-1)/BLOCK_SIZE);
        dim3 dimBlock = dim3(BLOCK_SIZE, BLOCK_SIZE);
        coef_mul_and_sub_kernel<<<dimGrid, dimBlock>>>(d_a, row+1, row+1,  d_coefs, n);

    }
    swap_vector[n-1] = n-1;
    cudaMemcpy(a, d_a, size, cudaMemcpyDeviceToHost);
    print_matrix(a, n);

    int* p = (int*)malloc(sizeof(int)*n);
    for (int i = 0; i < n; i++)
        p[i] = i;
    for (int i = n-1; i >= 0; i--) {
        int tmp = p[i];
        p[i] = p[swap_vector[i]];
        p[swap_vector[i]] = tmp;
    }
    for (int i = 0; i < n; i++)
        printf("%d ", p[i]);

    cudaFree(d_a);
    cudaFree(coefs);
    free(a);
    free(p);
    free(swap_vector);
    
    return 0;
}
