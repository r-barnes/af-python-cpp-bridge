#!/usr/bin/env python3
import arrayfire as af
import numpy as np
import ctypes
import testlib

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

print("Loop", flush=True)
for x in range(10):
    b = testlib.testfunc(ctypes.addressof(afvan.arr), ctypes.addressof(afthr.arr))
    c = af.array.Array(src=b, dims=afvan.shape, dtype=af.Dtype.f32, is_device=True)
    af.device.lock_array(c) #TODO: Do I need to do this to take ownership of the memory?