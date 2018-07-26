#include "stdio.h"
#include "stdlib.h"

#define SHARED_MEMORY_MAX_SIZE 1024
#define UINT_SIZE 32

#define BANKS_NUM 32
#define LOG_BANKS_NUM 5

#define CONFLICT_FREE_OFFSET(n) \
    (n >>  + n >> (2 * LOG_BANKS_NUM))

#define ERROR_HANDLING(call) {                                                                                                          \
    cudaError error = call;                                                                                             \
    if(error != cudaSuccess) {                                                                                  \
        fprintf(stderr, "ERROR: file '%s' in line %i: %s.\n",   \
            __FILE__, __LINE__, cudaGetErrorString(error));                             \
        exit(1);                                                                                                                \
    }                                                                                                                                   \
} while (0)


__device__ __host__
void print_array(int* a, int n) {
    for (int i = 0; i < n; i++)
        printf("%d ", a[i]);
    printf("\n");
}


__global__
void scan(int *a, int *s, int n, int all_n)
{
    extern __shared__ int temp[];

    int th_id = threadIdx.x;
    int th_offset = 2*(blockIdx.y*gridDim.x*blockDim.x + blockIdx.x*blockDim.x);
    int offset = 1;
    int leftIdx = th_id;
    int rightIdx = th_id + (n/2);

    int bankLeftOffset = CONFLICT_FREE_OFFSET(leftIdx);
    int bankRightOffset = CONFLICT_FREE_OFFSET(rightIdx);

    if (th_offset + th_id+(n/2) < all_n+1) {
        temp[leftIdx + bankLeftOffset] = a[th_offset+leftIdx];
        temp[rightIdx + bankRightOffset] = a[th_offset+rightIdx];

        for (int d = n/2; d > 0; d /= 2)
        {
            __syncthreads();
            if (th_id < d)
            {
                int leftIdx = offset*(2*th_id+1)-1;
                int rightIdx = offset*(2*th_id+2)-1;
                leftIdx += CONFLICT_FREE_OFFSET(leftIdx);
                rightIdx += CONFLICT_FREE_OFFSET(rightIdx);

                temp[rightIdx] += temp[leftIdx];
            }
            offset *= 2;
        }
        if (th_id==0)
            temp[n - 1 + CONFLICT_FREE_OFFSET(n - 1)] = 0;

        for (int d = 1; d < n; d *= 2)
        {
            offset /= 2;
            __syncthreads();
            if (th_id < d)
            {
                int leftIdx = offset*(2*th_id+1)-1;
                int rightIdx = offset*(2*th_id+2)-1;
                leftIdx += CONFLICT_FREE_OFFSET(leftIdx);
                rightIdx += CONFLICT_FREE_OFFSET(rightIdx);

                int tmp = temp[leftIdx];
                temp[leftIdx] = temp[rightIdx];
                temp[rightIdx] += tmp;
            }
        }
        __syncthreads();

        s[th_offset+rightIdx] = temp[rightIdx + bankRightOffset];
        if (th_id != 0)
            s[th_offset+leftIdx] = temp[leftIdx + bankLeftOffset];

        if (th_id == ((n/2)-1))
            s[th_offset+rightIdx+1] = s[th_offset+rightIdx] + a[th_offset+rightIdx];
    }
}


__device__ __host__
int min2(int a, int b) {
    return a < b? a:b;
}


__global__
void get_last_elements(int* a, int* last_elements, int n, int block_size, int a_len) {
    int idx = threadIdx.x + blockIdx.x*blockDim.x;
    int offset = blockDim.x * gridDim.x;
    for (int i = idx; i < n; i+=offset) {
        last_elements[i] = a[min2(i * block_size + block_size, a_len)];
    }
}

__global__
void sub(int* a, int* b, int n) {
    int idx = threadIdx.x + blockIdx.x*blockDim.x;
    int offset = blockDim.x * gridDim.x;
    for (int i = idx; i < n; i+=offset)
        a[i] = a[i] - b[i];
}

__global__
void sum(int* s, int* diff, int n) {
    int blockIdx2sum = blockIdx.y*gridDim.x + blockIdx.x;
    int thIdx = blockIdx.y*gridDim.x*blockDim.x + blockIdx.x*blockDim.x + threadIdx.x;
    if (thIdx < n)
        s[thIdx] += diff[blockIdx2sum];
}

void full_scan(int* a, int* s, int n) {
    if (n > SHARED_MEMORY_MAX_SIZE) {
        int blocks_count = (n+SHARED_MEMORY_MAX_SIZE-1)/SHARED_MEMORY_MAX_SIZE;
        int max_blocks_per_axis = 32768;
        if ((n % SHARED_MEMORY_MAX_SIZE) != 0) {
            int* tmp_s, *tmp_a;
            int* last_block_elements;
            ERROR_HANDLING(cudaMalloc(&last_block_elements, sizeof(n)*blocks_count));
            int threadblocks_count_y = blocks_count % max_blocks_per_axis == 0? blocks_count/max_blocks_per_axis : blocks_count/max_blocks_per_axis+1;
            int threadblocks_count_x = blocks_count <= max_blocks_per_axis? blocks_count : max_blocks_per_axis;

            dim3 dimGrid(threadblocks_count_x, threadblocks_count_y);
            int new_n = n + (SHARED_MEMORY_MAX_SIZE - n % SHARED_MEMORY_MAX_SIZE);
            size_t new_size = sizeof(int)*new_n;
            ERROR_HANDLING(cudaMalloc(&tmp_a, new_size));
            ERROR_HANDLING(cudaMalloc(&tmp_s, new_size+sizeof(int)));
            ERROR_HANDLING(cudaMemcpy(tmp_a, a, n*sizeof(int), cudaMemcpyDeviceToDevice));
            ERROR_HANDLING(cudaMemset(tmp_a+n, 0, sizeof(int)*(SHARED_MEMORY_MAX_SIZE - n % SHARED_MEMORY_MAX_SIZE)));
            ERROR_HANDLING(cudaMemset(tmp_s, 0, new_size+sizeof(int)));
	    ERROR_HANDLING(cudaGetLastError());
            scan <<<dimGrid, SHARED_MEMORY_MAX_SIZE/2, SHARED_MEMORY_MAX_SIZE*sizeof(int)>>>(tmp_a, tmp_s, SHARED_MEMORY_MAX_SIZE, new_n);
            ERROR_HANDLING(cudaGetLastError());

            ERROR_HANDLING(cudaMemcpy(s, tmp_s, (n+1)*sizeof(int), cudaMemcpyDeviceToDevice));
            ERROR_HANDLING(cudaFree(tmp_a));
            ERROR_HANDLING(cudaFree(tmp_s));
        }
        else {
            int threadblocks_count_y = blocks_count % max_blocks_per_axis == 0? blocks_count/max_blocks_per_axis : blocks_count/max_blocks_per_axis+1;
            int threadblocks_count_x = blocks_count <= max_blocks_per_axis? blocks_count : max_blocks_per_axis;
            dim3 dimGrid(
                    threadblocks_count_x,
                    threadblocks_count_y);
            scan <<< dimGrid, SHARED_MEMORY_MAX_SIZE/2, SHARED_MEMORY_MAX_SIZE*sizeof(int)>>>(a, s, SHARED_MEMORY_MAX_SIZE, n);
            ERROR_HANDLING(cudaGetLastError());
        }

        int* last_block_elements;
        ERROR_HANDLING(cudaMalloc(&last_block_elements, sizeof(n)*blocks_count));
        get_last_elements<<<1024, 256>>>(s, last_block_elements, blocks_count, SHARED_MEMORY_MAX_SIZE, n);
        ERROR_HANDLING(cudaGetLastError());
        int* new_s;
        ERROR_HANDLING(cudaMalloc(&new_s, sizeof(int)*(blocks_count+1)));
        ERROR_HANDLING(cudaMemset(new_s, 0, sizeof(int)*(blocks_count+1)));

        full_scan(last_block_elements, new_s, blocks_count);

        sub<<<1024, 256>>>(new_s+1, last_block_elements, blocks_count);
        ERROR_HANDLING(cudaGetLastError());

        int threadblocks_count_y = blocks_count % max_blocks_per_axis == 0? blocks_count/max_blocks_per_axis : blocks_count/max_blocks_per_axis+1;
        int threadblocks_count_x = blocks_count <= max_blocks_per_axis? blocks_count : max_blocks_per_axis;

        dim3 dimGrid(threadblocks_count_x, threadblocks_count_y);

        sum<<<dimGrid, SHARED_MEMORY_MAX_SIZE>>>(s+1, new_s+1, n);
        ERROR_HANDLING(cudaGetLastError());
    }
    else {
        dim3 dimGrid(1, 1);
        if ((n % SHARED_MEMORY_MAX_SIZE) != 0) {
            int* tmp_s, *tmp_a;
            size_t new_size = sizeof(int)*SHARED_MEMORY_MAX_SIZE;
            ERROR_HANDLING(cudaMalloc(&tmp_a, new_size));
            ERROR_HANDLING(cudaMalloc(&tmp_s, new_size+sizeof(int)));
            ERROR_HANDLING(cudaMemcpy(tmp_a, a, n*sizeof(int), cudaMemcpyDeviceToDevice));
            ERROR_HANDLING(cudaMemset(tmp_a+n, 0, sizeof(int)*(SHARED_MEMORY_MAX_SIZE - n % SHARED_MEMORY_MAX_SIZE)));
            ERROR_HANDLING(cudaMemset(tmp_s, 0, sizeof(int)*(SHARED_MEMORY_MAX_SIZE+1)));

            scan <<<dimGrid, SHARED_MEMORY_MAX_SIZE/2, new_size>>>(tmp_a, tmp_s, SHARED_MEMORY_MAX_SIZE, SHARED_MEMORY_MAX_SIZE);
            ERROR_HANDLING(cudaGetLastError());
            cudaMemcpy(s+1, tmp_s+1, n*sizeof(int), cudaMemcpyDeviceToDevice);
            cudaFree(tmp_a);
            //cudaFree(tmp_s);
        }
        else {
            scan <<<dimGrid, SHARED_MEMORY_MAX_SIZE/2, n*sizeof(int)>>>(a, s, n, n);
            ERROR_HANDLING(cudaGetLastError());
        }
    }
}


__global__
void get_digit(uint *a, int *a_digits, int digit_number, int n) {
    int idx = blockDim.x*blockIdx.x + threadIdx.x;
    int offset = blockDim.x*gridDim.x;
    for (int i = idx; i < n; i+=offset) {
        a_digits[i] = (a[i]>>digit_number) & 1;
    }
}

__global__
void set_new_position(uint *a_out, uint *a_in, int *s, int *b, int n) {
    int idx = blockDim.x*blockIdx.x + threadIdx.x;
    int offset = blockDim.x*gridDim.x;
    for (int i = idx; i < n; i+=offset) {
        int new_pos = (b[i] == 0? i-s[i]: s[i] + n-s[n]);
        a_out[new_pos] = a_in[i];
    }
}


int main() {
    int n;
    fread(&n, sizeof(int), 1, stdin);

    int size = n*sizeof(int);

    uint* a = (uint*)malloc(size);
    fread(a, sizeof(uint), n, stdin);


    int* ds;
    uint *da;
    uint* da2;
    int *da_digits;
    cudaMalloc(&ds, size+sizeof(int));
    cudaMalloc(&da, size);
    cudaMalloc(&da_digits, size);
    
    cudaMemcpy(da, a, size, cudaMemcpyHostToDevice);

    for (int digit_number = 0; digit_number < UINT_SIZE; digit_number++) {
        get_digit <<<1024, 256>>>(da, da_digits, digit_number, n);
	cudaFree(da);
        cudaMemset(ds, 0, size+sizeof(int));
        full_scan(da_digits, ds, n);
        ERROR_HANDLING(cudaGetLastError());
	ERROR_HANDLING(cudaMalloc(&da, size));
        ERROR_HANDLING(cudaMalloc(&da2, size));
        ERROR_HANDLING(cudaMemcpy(da, a, size, cudaMemcpyHostToDevice));
        ERROR_HANDLING(cudaMemcpy(da2, da, size, cudaMemcpyDeviceToDevice));
        
        set_new_position <<<1024, 256>>>(da, da2, ds, da_digits, n);
	ERROR_HANDLING(cudaMemcpy(a, da, size, cudaMemcpyDeviceToHost));
        cudaFree(da2);
    }
    //cudaMemcpy(a, da, size, cudaMemcpyDeviceToHost);
    fwrite(a, sizeof(uint), n, stdout);

    cudaFree(da);
    cudaFree(ds);
    cudaFree(da_digits);


    free(a);
    return 0;
}
