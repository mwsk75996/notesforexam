# Mini templates

## CMake med MQTT, Catch2 og spdlog

```cmake
cmake_minimum_required(VERSION 3.10)
project(programmering)

set(CMAKE_CXX_STANDARD 17)

find_package(spdlog REQUIRED)

add_executable(publisher src/publisher.cpp)
add_executable(subscriber src/subscriber.cpp)

target_compile_options(publisher PUBLIC -Wall -Wextra -Wfloat-conversion)
target_compile_options(subscriber PUBLIC -Wall -Wextra -Wfloat-conversion)

target_include_directories(publisher PUBLIC src)
target_include_directories(subscriber PUBLIC src)

target_link_libraries(publisher paho-mqttpp3 paho-mqtt3as spdlog::spdlog)
target_link_libraries(subscriber paho-mqttpp3 paho-mqtt3as spdlog::spdlog)

find_package(Catch2 REQUIRED)

file(GLOB_RECURSE sources_test tests/*.cpp)
add_executable(tests ${sources_test})
target_link_libraries(tests Catch2Main Catch2)

include(Catch)
catch_discover_tests(tests)
enable_testing()
```

## run_pub.sh

```sh
#!/usr/bin/env sh
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

cmake -S "$SCRIPT_DIR" -B "$SCRIPT_DIR/build"
cmake --build "$SCRIPT_DIR/build" --target publisher
"$SCRIPT_DIR/build/publisher"
```

## run_sub.sh

```sh
#!/usr/bin/env sh
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

cmake -S "$SCRIPT_DIR" -B "$SCRIPT_DIR/build"
cmake --build "$SCRIPT_DIR/build" --target subscriber
"$SCRIPT_DIR/build/subscriber"
```

## run_tests.sh

```sh
#!/usr/bin/env sh
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

cmake -S "$SCRIPT_DIR" -B "$SCRIPT_DIR/build"
cmake --build "$SCRIPT_DIR/build" --target tests
"$SCRIPT_DIR/build/tests"
```

## Simpel Catch2 test

```cpp
#include <catch2/catch_test_macros.hpp>

bool isTemperatureValid(double temp) {
    return temp >= 10.0 && temp <= 30.0;
}

TEST_CASE("temperature must be between 10 and 30", "[temperature]") {
    CHECK(isTemperatureValid(10.0));
    CHECK(isTemperatureValid(20.0));
    CHECK(isTemperatureValid(30.0));

    CHECK_FALSE(isTemperatureValid(9.9));
    CHECK_FALSE(isTemperatureValid(30.1));
}
```
