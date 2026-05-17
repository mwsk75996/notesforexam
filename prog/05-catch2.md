# Catch2

Catch2 bruges til unit tests i C++.

Hvis projektet bruger GoogleTest i stedet, se `11-googletest-ci.md`.

Include:

```cpp
#include <catch2/catch_test_macros.hpp>
```

Simpel test:

```cpp
#include <catch2/catch_test_macros.hpp>

int add(int a, int b) {
    return a + b;
}

TEST_CASE("add returns sum") {
    REQUIRE(add(2, 3) == 5);
}
```

`REQUIRE` stopper testen med det samme hvis den fejler.

`CHECK` fortsætter testen selvom den fejler.

```cpp
CHECK(value > 0);
REQUIRE(pointer != nullptr);
```

Negative checks:

```cpp
CHECK_FALSE(name.empty());
REQUIRE_FALSE(hasError);
```

Tags er gode til at gruppere tests:

```cpp
TEST_CASE("temperature is valid", "[publisher]") {
    CHECK(isTemperatureValid(20.0));
}
```

CMake med Catch2:

```cmake
find_package(Catch2 REQUIRED)

file(GLOB_RECURSE sources_test tests/*.cpp)

add_executable(tests ${sources_test})
target_link_libraries(tests Catch2Main Catch2)

include(Catch)
catch_discover_tests(tests)
enable_testing()
```

Nyere Catch2-installationer bruger ofte target-navne med namespace:

```cmake
target_link_libraries(tests PRIVATE Catch2::Catch2WithMain)
```

Byg og kør tests:

```sh
cmake -S . -B build
cmake --build build
./build/tests
```

Hvis du vil se mere output:

```sh
./build/tests -s
```

Kør kun tests med et bestemt tag:

```sh
./build/tests "[publisher]"
```

Eksempel på test af parsing/validering:

```cpp
#include <catch2/catch_test_macros.hpp>

#include <string>

bool shouldSubscribe(const std::string& topic, int qos) {
    return !topic.empty() && qos >= 0 && qos <= 2;
}

TEST_CASE("subscriber config is valid", "[subscriber]") {
    CHECK(shouldSubscribe("test", 0));
    CHECK(shouldSubscribe("sensor/room1", 1));

    CHECK_FALSE(shouldSubscribe("", 1));
    CHECK_FALSE(shouldSubscribe("test", 3));
}
```

God eksamensforklaring:

Tests bruges til at bevise at små dele af programmet virker isoleret. Det er især smart til funktioner som validering, parsing, hashing og payload-format.
