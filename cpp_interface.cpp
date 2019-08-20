#include <pybind11/pybind11.h>
#include <arrayfire.h>
#include <af/macros.h>
#include <cmath>
#include <iostream>

uint64_t get_gpu_pointer(af::array &arr){
    const auto adr = reinterpret_cast<uint64_t>(arr.device<void>());
    arr.unlock();
    return adr;
}

uint64_t testfunc(
    uint64_t input_ptr,
    uint64_t input2_ptr
){
    std::cout<<"\n\n###############C++"<<std::endl;
    // AF_MEM_INFO("before test");
    af_print_mem_info("before test", 0);

    af::array input (*(af_array**)input_ptr);
    af::array input2(*(af_array**)input2_ptr);

    std::cout<<"input_ptr="<<std::hex<<get_gpu_pointer(input)<<std::endl;
    std::cout<<"input2_ptr="<<std::hex<<get_gpu_pointer(input2)<<std::endl;

    af::array out = input*input2;

    af_print_mem_info("after test", 0);
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
