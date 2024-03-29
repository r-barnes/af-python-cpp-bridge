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

af::array external_pointer_to_internal_array(const uint64_t input_ptr){
    //Cast pointer to af_array
    af_array arr = reinterpret_cast<af_array>(input_ptr);    

    //Increment the array's reference count so when af::array goes out of scope
    //it doesn't scrub the array's memory.
    af_array temp_ref;
    af_retain_array(&temp_ref, arr);

    return af::array(temp_ref);
}

uint64_t testfunc(
    uint64_t input_ptr,
    uint64_t input2_ptr
){
    std::cout<<"\n\n###############C++"<<std::endl;
    // AF_MEM_INFO("before test");
    af_print_mem_info("before test", 0);

    std::cout<<"input_ptr afarr="<<std::hex<<(input_ptr)<<std::endl;
    std::cout<<"input2_ptr afarr="<<std::hex<<(input2_ptr)<<std::endl;

    auto input = external_pointer_to_internal_array(input_ptr);
    auto input2 = external_pointer_to_internal_array(input2_ptr);

    std::cout<<"input_ptr gpu="<<std::hex<<get_gpu_pointer(input)<<std::endl;
    std::cout<<"input2_ptr gpu="<<std::hex<<get_gpu_pointer(input2)<<std::endl;

    af::array out = input*input2;

    af_print_mem_info("after test", 0);
    //Need to return device pointer since otherwise af_array reaches end of
    //life, likely before it can be saved by getting reinstantiated
    af_array out_ptr;
    af_retain_array(&out_ptr, out.get());
    std::cout<<"out_ptr is "<<std::hex<<out_ptr<<std::endl;
    return reinterpret_cast<uint64_t>(out_ptr);
}

PYBIND11_MODULE(testlib, m) {
    m.doc() = "core functions";

    af::setBackend(AF_BACKEND_CUDA);
    af::setDevice(0);
    af_info();

    m.def("testfunc", &testfunc, "TODO desc");
}
