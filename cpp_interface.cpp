#include <pybind11/pybind11.h>
#include <arrayfire.h>
#include <cmath>
#include <iostream>
#include "kernels.h"

uint64_t testfunc(
    uint64_t input_ptr,
    uint64_t input2_ptr,
    const int width,
    const int height
){
    const int size=width*height;
    std::cout<<"input_ptr = "<<input_ptr<<std::endl;
    // The Gerchberg-Saxon update (GS update) is in fact gradient descent with step size 1
    af::array input(*(void**)input_ptr);
    af::array input2(*(void**)input2_ptr);

    input *= input2;

    std::cout<<__LINE__<<std::endl;
    return reinterpret_cast<uint64_t>(input.copy().device<float>());
}

PYBIND11_MODULE(testlib, m) {
    m.doc() = "core functions";

    af::setBackend(AF_BACKEND_CUDA);
    af::setDevice(0);

    m.def("testfunc", &testfunc, "TODO desc");
}