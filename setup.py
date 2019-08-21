from setuptools import *
# from distutils.core import setup
# from distutils.extension import Extension
from Cython.Distutils import build_ext

setup(
  name = 'Demos',
  ext_modules=[
    Extension("test",
              libraries = ["afcuda"],
              sources=["test.pyx", "cpp_interface.cpp"],
              language="c++"),
    ],
  cmdclass = {'build_ext': build_ext},
)