cmake_minimum_required(VERSION 3.10)
project(MariaCPP)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(PkgConfig REQUIRED)
pkg_check_modules(MARIADB REQUIRED libmariadb)

add_executable(main src/main.cpp)
target_compile_options(main PRIVATE -Wall -Wextra -Wpedantic)
target_include_directories(main PRIVATE ${MARIADB_INCLUDE_DIRS})
target_link_directories(main PRIVATE ${MARIADB_LIBRARY_DIRS})
target_link_libraries(main PRIVATE ${MARIADB_LIBRARIES})

add_executable(tests tests/test_connection.cpp)
target_compile_options(tests PRIVATE -Wall -Wextra -Wpedantic)
target_include_directories(tests PRIVATE ${MARIADB_INCLUDE_DIRS})
target_link_directories(tests PRIVATE ${MARIADB_LIBRARY_DIRS})
target_link_libraries(tests PRIVATE ${MARIADB_LIBRARIES})

enable_testing()
add_test(NAME mariadb_client_smoke_test COMMAND tests)
