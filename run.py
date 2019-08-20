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
    b = testlib.testfunc(ctypes.addressof(afvan.arr), ctypes.addressof(afthr.arr), 4, 4)
    print("back", flush=True)
    af.device.unlock_array(afvan)
    af.device.unlock_array(afthr)
    print("unlocked", flush=True)
    c = af.array.Array(src=b, dims=(4,4), dtype=af.Dtype.f32, is_device=True)
    print("wrapped", flush=True)
    print(c)