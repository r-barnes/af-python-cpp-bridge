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
    return out


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

print("afvan", hex(get_gpu_pointer(afvan)))
print("afthr", hex(get_gpu_pointer(afthr)))

print("\n\nLoop", flush=True)
for x in range(10):
    af.device.print_mem_info("top of the loop")
    b = testlib.testfunc(ctypes.addressof(afvan.arr), ctypes.addressof(afthr.arr))
    print("\n\n################Python", flush=True)
    af.device.print_mem_info("back in python")
    c = array_from_af_pointer(b)
    af.device.print_mem_info("after defining array")
