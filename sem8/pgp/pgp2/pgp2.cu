#include "stdio.h"
#include "stdlib.h"
#include <cmath>
using namespace std;
#define ERROR_HANDLING(call) {														\
    cudaError error = call;												\
    if(error != cudaSuccess) {											\
        fprintf(stderr, "ERROR: in file '%s' in line %i: %s.\n",	\
            __FILE__, __LINE__, cudaGetErrorString(error));				\
        exit(1);														\
    }																	\
} while (0)

texture<uchar4, 2, cudaReadModeElementType> texRef2D;

__device__
double getBrightnessFromRGB(uchar4 p) {
	return 0.299*p.x + 0.587*p.y + 0.114*p.z;
}

__device__
int convolution(double window[3][3]) {
	double Gx = window[0][2] - window[0][0] + window[1][2] - window[1][0] + window[2][2] - window[2][0];
	double Gy = window[2][0] - window[0][0] + window[2][1] - window[0][1] + window[2][2] - window[0][2];

	double eps = 1e-10;
	double G = sqrt(Gx*Gx+Gy*Gy);
	int res =  abs(((int)G+1.0)-G)<eps ? (int)G+1 : (int)G;
	if (res < 0)
		res = 0;
	else if (res > 255)
		res = 255;
	return res;
}


__global__
void PrewittKernel(uchar4 *device_data, int width, int height) {
	int idx = threadIdx.x + blockIdx.x * blockDim.x;
	int idy = threadIdx.y + blockIdx.y * blockDim.y;
	int offsetx = blockDim.x * gridDim.x;
	int offsety = blockDim.y * gridDim.y;
	int x, y;
    const int windowWidth = 3;
    const int windowHeight = 3;
	for(x = idx; x < width; x += offsetx) 
		for(y = idy; y < height; y += offsety) {
			uchar4 windowPoints[windowHeight][windowWidth];
			uchar4 centerPoint = tex2D(texRef2D, x, y);
			windowPoints[0][0] = tex2D(texRef2D, x-1, y-1);
			windowPoints[0][1] = tex2D(texRef2D, x, y-1);
			windowPoints[0][2] = tex2D(texRef2D, x+1, y-1);
			windowPoints[1][0] = tex2D(texRef2D, x-1, y);
			windowPoints[1][1] = centerPoint;
			windowPoints[1][2] = tex2D(texRef2D, x+1, y);
			windowPoints[2][0] = tex2D(texRef2D, x-1, y+1);
			windowPoints[2][1] = tex2D(texRef2D, x, y+1);
			windowPoints[2][2] = tex2D(texRef2D, x+1, y+1);
			double windowBrightnesses[windowWidth][windowHeight];
			for (int i = 0; i < windowHeight; i++)
				for (int j = 0; j < windowWidth; j++) {
					windowBrightnesses[i][j] = getBrightnessFromRGB(windowPoints[i][j]);
			}

			int resBrightness = convolution(windowBrightnesses);
			uchar4 resPoint = make_uchar4(resBrightness, resBrightness, resBrightness, centerPoint.w);
			device_data[y * width + x] = resPoint;
		}
}

int main(int argc, char *argv[]) {
	int width, height;
    char inputFilename[256];
    char outputFilename[256];
    scanf("%s", inputFilename);
    scanf("%s", outputFilename);	
    FILE* file = fopen(inputFilename, "rb");

	fread(&width, sizeof(int), 1, file);
	fread(&height, sizeof(int), 1, file);
	uchar4* io_data = (uchar4*)malloc(sizeof(uchar4)*height*width);
	
	fread(io_data, sizeof(uchar4), width*height, file);
	fclose(file);

	cudaArray *c_arr;
	cudaChannelFormatDesc ch = cudaCreateChannelDesc<uchar4>();
	ERROR_HANDLING(cudaMallocArray(&c_arr, &ch, width, height));
	ERROR_HANDLING(cudaMemcpyToArray(c_arr, 0, 0, io_data, sizeof(uchar4) * width * height, cudaMemcpyHostToDevice));

	texRef2D.addressMode[0] = cudaAddressModeClamp;
	texRef2D.addressMode[1] = cudaAddressModeClamp;
	texRef2D.channelDesc = ch;
	texRef2D.filterMode = cudaFilterModePoint;
	texRef2D.normalized = false;


	ERROR_HANDLING(cudaBindTextureToArray(texRef2D, c_arr, ch));
	
	uchar4 *dev_data;
	ERROR_HANDLING(cudaMalloc(&dev_data, sizeof(uchar4) * width * height));

	PrewittKernel<<<dim3(32, 32), dim3(16, 16)>>>(dev_data, width, height);
	ERROR_HANDLING(cudaGetLastError());

	ERROR_HANDLING(cudaMemcpy(io_data, dev_data, sizeof(uchar4) * width * height, cudaMemcpyDeviceToHost));
	ERROR_HANDLING(cudaUnbindTexture(texRef2D));
	ERROR_HANDLING(cudaFreeArray(c_arr));
	ERROR_HANDLING(cudaFree(dev_data));

	file = fopen(outputFilename, "wb");
	fwrite(&width, sizeof(int), 1, file);
	fwrite(&height, sizeof(int), 1, file);
	fwrite(io_data, sizeof(uchar4), width * height, file);
	fclose(file);
    free(io_data);
	return 0;
} 
