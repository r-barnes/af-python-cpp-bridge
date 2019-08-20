#pragma once

#include <cuda_fp16.h>

void absify(float *amp, af::cfloat const *const spectrum, const int n);
void rescale(float amp_max, af::cfloat *spectrum, af::cfloat const *const amp_meas, float const *const amp, const int n);