#!/usr/bin/env python3
import arrayfire as af
import numpy as np
import ctypes
import testlib

def get_gpu_pointer(x):
    adr = af.device.get_device_ptr(x)
    af.device.unlock_array(x)
    return adr.value

def array_from_af_pointer(af_array_ptr):
    out = af.Array()
    out.arr = ctypes.c_void_p(af_array_ptr)
    print("Converting from ",hex(af_array_ptr))
    # print("New array has device pointer ",hex(get_gpu_pointer(out)))
    return out

def get_use_count(arr):
    uses = ctypes.c_int(0)
    af.safe_call(af.backend.get().af_get_data_ref_count(af.c_pointer(uses), arr.arr))
    return uses

# use gpu backend
af.set_backend('cuda')
af.set_device(0)  # select the gpu to use
af.info()

van = np.array([1, 2, 3, 5])
van = np.vander(van)
two = np.ones((4,4))*2

print("Define stuff", flush=True)
afvan = af.interop.from_ndarray(van)
afvan = afvan.as_type(af.Dtype.f32)

afthr = af.interop.from_ndarray(two)
afthr = afthr.as_type(af.Dtype.f32)

af.device.print_mem_info("before loops")

print("afvan", hex(get_gpu_pointer(afvan)), " ", get_use_count(afvan), flush=True)
print("afthr", hex(get_gpu_pointer(afthr)), " ", get_use_count(afthr), flush=True)

print("\n\nLoop", flush=True)
for x in range(10):
    af.device.print_mem_info("top of the loop")
    b = testlib.testfunc(ctypes.addressof(afvan.arr), ctypes.addressof(afthr.arr))
    print("\n\n################Python", flush=True)
    print("afvan", hex(get_gpu_pointer(afvan)), " ", get_use_count(afvan), flush=True)
    print("afthr", hex(get_gpu_pointer(afthr)), " ", get_use_count(afthr), flush=True)
    af.device.print_mem_info("back in python")
    c = array_from_af_pointer(b)
    af.device.print_mem_info("after defining array")
    print("afvan", hex(get_gpu_pointer(afvan)), " ", get_use_count(afvan), flush=True)
    print("afthr", hex(get_gpu_pointer(afthr)), " ", get_use_count(afthr), flush=True)
    print("c",     hex(get_gpu_pointer(c)),     " ", get_use_count(c), flush=True)
