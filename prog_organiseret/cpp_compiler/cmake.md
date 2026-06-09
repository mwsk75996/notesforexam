# CMake

CMake bruges til at beskrive hvordan projektet skal bygges. Man bygger normalt ikke direkte med `g++`, men lader CMake lave build-filerne.

Standard workflow:

```sh
cmake -S . -B build
cmake --build build
./build/program
```

`-S .` betyder source folder er den nuværende mappe.

`-B build` betyder build output skal ligge i `build/`.

Minimal `CMakeLists.txt`:

```cmake
cmake_minimum_required(VERSION 3.10)
project(my_project)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_executable(app src/main.cpp)
```

Med warnings:

```cmake
target_compile_options(app PRIVATE -Wall -Wextra -Wfloat-conversion)
```

Med include folder:

```cmake
target_include_directories(app PRIVATE src)
```

Med libraries:

```cmake
target_link_libraries(app paho-mqttpp3 paho-mqtt3as)
```

Eksempel med flere source filer:

```text
src/
  main.cpp
  helper.cpp
  helper.hpp
```

```cmake
add_executable(app
    src/main.cpp
    src/helper.cpp
)

target_include_directories(app PRIVATE src)
```

Flere executables:

```cmake
add_executable(publisher src/publisher.cpp)
add_executable(subscriber src/subscriber.cpp)

target_link_libraries(publisher paho-mqttpp3 paho-mqtt3as)
target_link_libraries(subscriber paho-mqttpp3 paho-mqtt3as)
```

Byg kun et bestemt target:

```sh
cmake --build build --target publisher
cmake --build build --target subscriber
```

Debug build:

```sh
cmake -S . -B build -DCMAKE_BUILD_TYPE=Debug
cmake --build build
```

Hvis CMake opfører sig mærkeligt, slet build-mappen og prøv igen:

```sh
rm -rf build
cmake -S . -B build
cmake --build build
```
