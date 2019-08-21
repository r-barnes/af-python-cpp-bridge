all:
	python3 setup.py build_ext --inplace

clean:
	rm -rf build/ test.cpp test.cpython-36m-x86_64-linux-gnu.so