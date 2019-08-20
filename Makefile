#[1/2] /usr/bin/c++  -Dpathai_EXPORTS -I../submodules/pybind11/include -I/usr/include/python3.6m -fPIC -fvisibility=hidden   -std=c++14 -flto -fno-fat-lto-objects -std=gnu++14 -MD -MT src/CMakeFiles/pathai.dir/442.cpp.o -MF src/CMakeFiles/pathai.dir/442.cpp.o.d -o src/CMakeFiles/pathai.dir/442.cpp.o -c ../src/442.cpp

#[2/2] : && /usr/bin/c++ -fPIC    -shared  -o src/pathai.cpython-36m-x86_64-linux-gnu.so src/CMakeFiles/pathai.dir/442.cpp.o  -flto -lafcuda && :

all: cpp_interface.o
	g++-6 -g -o testlib.so -shared -fPIC cpp_interface.o -flto -lafcuda -lcudart -Wall -Wextra

cpp_interface.o: cpp_interface.cpp
	g++-6 -g -fPIC -c cpp_interface.cpp -I/usr/include/python3.6m -Isubmodules/pybind11/include -lafcuda -laf -Wall -Wextra -fvisibility=hidden

clean:
	rm -rf *.o *.so

# g++-6 -o pathai.so -O3 -Wall -shared -std=c++14 -fPIC 