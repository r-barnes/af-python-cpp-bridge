#include <pybind11/pybind11.h>
#include <arrayfire.h>
#include <cmath>
#include <iostream>

uint64_t testfunc(
    uint64_t input_ptr,
    uint64_t input2_ptr
){
    af::array input (*(af_array**)input_ptr);
    af::array input2(*(af_array**)input2_ptr);

    af::array out = input*input2;

    //Need to return device pointer since otherwise af_array reaches end of
    //life, likely before it can be saved by getting reinstantiated
    return reinterpret_cast<uint64_t>(out.device<float>());
}

PYBIND11_MODULE(testlib, m) {
    m.doc() = "core functions";

    af::setBackend(AF_BACKEND_CUDA);
    af::setDevice(0);
    af_info();

    m.def("testfunc", &testfunc, "TODO desc");
}