#include <stdexcept>
#include <string>
#include <arrayfire.h>
#include <iostream>
#include <af/cuda.h>
#include <cuda_fp16.h>
typedef float2 cuFloatComplex;
typedef cuFloatComplex cfloat;

__global__
void absify_cuda(float *amp, cfloat const *const spectrum, const int n)
{
    for (int i = blockIdx.x * blockDim.x + threadIdx.x; i < n; i += blockDim.x * gridDim.x){
        amp[i] = hypotf(spectrum[i].x, spectrum[i].y);
    }
}

void absify(float *amp, af::cfloat const *const spectrum, const int n){
  int const af_id             = af::getDevice();
  int const cuda_id           = afcu::getNativeId(af_id);
  cudaStream_t af_cuda_stream = afcu::getStream(cuda_id);

  std::cout<<"Absify on "<<amp<<" and "<<spectrum<<std::endl;
  absify_cuda<<<16384,256,0,af_cuda_stream>>>(amp, reinterpret_cast<cfloat const *>(spectrum), n);
  const auto ret = cudaDeviceSynchronize();
  if(ret!=cudaSuccess){
    throw std::runtime_error(std::string("Kernel absify failed! ") + cudaGetErrorString(cudaGetLastError()));
  }
}



#define __cabsf(in) hypotf(in.x, in.y)

__device__ cfloat __cplx2f(float x, float y) {
    cfloat res = {x, y};
    return res;
}

__device__ cfloat __cdivf(cfloat lhs, cfloat rhs) {
    // Normalize by absolute value and multiply
    float rhs_abs     = __cabsf(rhs);
    float inv_rhs_abs = 1.0f / rhs_abs;
    float rhs_x       = inv_rhs_abs * rhs.x;
    float rhs_y       = inv_rhs_abs * rhs.y;
    cfloat out = {lhs.x * rhs_x + lhs.y * rhs_y, lhs.y * rhs_x - lhs.x * rhs_y};
    out.x *= inv_rhs_abs;
    out.y *= inv_rhs_abs;
    return out;
}

__device__ cfloat __cmulf(cfloat lhs, cfloat rhs) {
    cfloat out;
    out.x = lhs.x * rhs.x - lhs.y * rhs.y;
    out.y = lhs.x * rhs.y + lhs.y * rhs.x;
    return out;
}


__global__
void rescale_cuda(float amp_max, cfloat *spectrum, cfloat const *const amp_meas, float const *const amp, const int n)
{
  for (int i = blockIdx.x * blockDim.x + threadIdx.x; i < n; i += blockDim.x * gridDim.x){
    float const maxv = fmax(amp_max, amp[i]);
    cfloat val5 = __cdivf(spectrum[i], __cplx2f(maxv, 0));
    cfloat val7 = __cmulf(val5, amp_meas[i]);
    spectrum[i] = val7;
  }
}

void rescale(float amp_max, af::cfloat *spectrum, af::cfloat const *const amp_meas, float const *const amp, const int n){
  int const af_id             = af::getDevice();
  int const cuda_id           = afcu::getNativeId(af_id);
  cudaStream_t af_cuda_stream = afcu::getStream(cuda_id);

  rescale_cuda<<<16384,256,0,af_cuda_stream>>>(amp_max, 
    reinterpret_cast<cfloat *>(spectrum),
    reinterpret_cast<cfloat const *>(amp_meas),
    amp,
    n
  );
  const auto ret = cudaDeviceSynchronize();
  if(ret!=cudaSuccess){
    throw std::runtime_error(std::string("Kernel rescale failed! ") + cudaGetErrorString(cudaGetLastError()));
  }
}
