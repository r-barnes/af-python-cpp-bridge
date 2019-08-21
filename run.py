#!/usr/bin/env python3
import arrayfire as af
import numpy as np
import ctypes
import test

# use gpu backend
af.set_backend('cuda')
af.set_device(0)  # select the gpu to use
af.info()

van = np.array([1, 2, 3, 5])
van = np.vander(van)

print("Define stuff", flush=True)
afvan = af.interop.from_ndarray(van)
afvan = afvan.as_type(af.Dtype.f32)

af.device.print_mem_info("before loops")

print("\n\nLoop", flush=True)
for x in range(10):
    af.device.print_mem_info("top of the loop")
    test.testfunc2(ctypes.addressof(afvan.arr))
    print("\n\n################Python", flush=True)
    af.device.print_mem_info("back in python")

print("end", flush=True)