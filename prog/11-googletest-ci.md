# GoogleTest og CI/CD

Repo-eksempel:

- [q_api_case](https://github.com/mwsk75996/q_api_case)

GoogleTest er et andet C++ test-framework. Det minder om Catch2, men bruger typisk `TEST` eller `TEST_F`.

## Simpel GoogleTest

```cpp
#include <gtest/gtest.h>

int add(int a, int b) {
    return a + b;
}

TEST(AddTest, ReturnsSum) {
    EXPECT_EQ(add(2, 3), 5);
}
```

`EXPECT_*` registrerer fejlen og fortsætter testen.

`ASSERT_*` stopper testen med det samme hvis den fejler.

## Test fixture

En fixture er god når flere tests skal bruge samme setup.

```cpp
#include <gtest/gtest.h>

class QualityServiceTest : public ::testing::Test {
protected:
    QualityService service;
};

TEST_F(QualityServiceTest, GradeBoundaries) {
    EXPECT_EQ(service.calculateGrade(59), "F");
    EXPECT_EQ(service.calculateGrade(60), "D");
    EXPECT_EQ(service.calculateGrade(101), "Ugyldig");
}
```

## CMake med FetchContent

`q_api_case` henter GoogleTest automatisk med CMake:

```cmake
include(FetchContent)
FetchContent_Declare(
  googletest
  URL https://github.com/google/googletest/archive/refs/tags/v1.14.0.zip
)
FetchContent_MakeAvailable(googletest)

enable_testing()

add_executable(tests tests/test.cpp)
target_link_libraries(tests PRIVATE GTest::gtest_main)

include(GoogleTest)
gtest_discover_tests(tests)
```

Kør tests:

```sh
cmake -S . -B build
cmake --build build
ctest --test-dir build --output-on-failure
```

## Black box-test

Black box-test betyder at man tester systemet udefra uden at kigge på implementationen.

Gode ting at teste:

- gyldige værdier
- ugyldige værdier
- grænseværdier lige under, på og over grænsen
- kombinationer af boolske flags

Eksempel:

```text
score: -1, 0, 1
score: 59, 60, 61
score: 99, 100, 101
```

## CI/CD med GitHub Actions

CI betyder at GitHub automatisk bygger og tester projektet når der pushes eller laves pull request.

Minimal C++ CI:

```yaml
name: Cpp CI

on:
  push:
  pull_request:

jobs:
  build-and-test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Install build tools
        run: sudo apt-get update && sudo apt-get install -y cmake g++ ninja-build

      - name: Configure
        run: cmake -S . -B build -G Ninja

      - name: Build
        run: cmake --build build

      - name: Test
        run: ctest --test-dir build --output-on-failure
```

God eksamensforklaring:

CI/CD gør build og tests automatiske, så fejl opdages tidligt. I `q_api_case` bruges GitHub Actions til build, GoogleTest/CTest og deploy af `web/` til GitHub Pages.
