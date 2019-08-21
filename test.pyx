cdef extern from "cpp_interface.h":
  cdef long long testfunc(long long input_ptr);

def testfunc2(input_ptr: int) -> int:
    return testfunc(input_ptr)
