cmake_minimum_required(VERSION 3.10) # setting this is required
project(publisher)                   # this sets the project name

set(CMAKE_CXX_STANDARD 17)

file(GLOB_RECURSE sources_test tests/*.c tests/*.cpp)

add_executable(publisher src/publisher.cpp)
add_executable(subscriber src/subscriber.cpp)

target_compile_options(publisher PUBLIC -Wall -Wfloat-conversion)
target_compile_options(subscriber PUBLIC -Wall -Wfloat-conversion)

target_include_directories(publisher PUBLIC src )
target_include_directories(subscriber PUBLIC src )

target_link_libraries(publisher paho-mqttpp3 paho-mqtt3as)
target_link_libraries(subscriber paho-mqttpp3 paho-mqtt3as)

file(COPY ${data} DESTINATION resources)

find_package(Catch2 REQUIRED)
add_executable(tests ${sources_test})
target_link_libraries(tests Catch2Main Catch2)
include(Catch)
catch_discover_tests(tests)
enable_testing()

# Installs the whole directory tree into DESTINATION as a package 
install(TARGETS publisher DESTINATION example_destination)
install(DIRECTORY resources DESTINATION example_destination)

set(CPACK_PACKAGE_NAME publisher)
set(CPACK_PACKAGE_VERSION "1.0.0")

set(CPACK_MONOLITHIC_INSTALL 1)

include(CPack)
