// #include <pybind11/pybind11.h>
#include <arrayfire.h>
#include <af/macros.h>
#include <cmath>
#include <iostream>

long long testfunc(long long input_ptr){
    std::cout<<"\n\n###############C++"<<std::endl;
    // AF_MEM_INFO("before test");
    af_print_mem_info("before test", 0);

    //Works with these lines
    {
        af_array in = *reinterpret_cast<af_array**>(input_ptr);
        af_array temp;

        af_copy_array (&temp, in);
        af::array input(temp);

        std::cout<<"Size = "<<input.dims(0)<<std::endl;
    }

    //Breaks with these lines
    // {
    //     af_array in = *reinterpret_cast<af_array**>(input_ptr);
    //     af::array input(in);

    //     std::cout<<"Size = "<<input.dims(0)<<std::endl;
    // }


    af_print_mem_info("after test", 0);
    return 0;
}
