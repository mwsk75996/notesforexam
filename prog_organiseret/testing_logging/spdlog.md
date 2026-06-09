# Logging med spdlog

Logging er bedre end bare `std::cout`, fordi man kan bruge levels og få pænere output.

Typiske levels:

- `trace`: meget detaljeret
- `debug`: debug info
- `info`: normal besked
- `warn`: noget er mærkeligt, men programmet kan fortsætte
- `error`: noget gik galt
- `critical`: alvorlig fejl

Include:

```cpp
#include <spdlog/spdlog.h>
```

Eksempel:

```cpp
#include <spdlog/spdlog.h>

int main() {
    double temp = 31.5;

    spdlog::info("Program started");
    spdlog::warn("Temperature is high: {}", temp);
    spdlog::error("Could not connect to broker");
}
```

Format med variabler:

```cpp
std::string topic = "test";
int qos = 1;

spdlog::info("Subscribing to topic '{}' with QoS {}", topic, qos);
```

Sæt log level:

```cpp
spdlog::set_level(spdlog::level::debug);

spdlog::debug("This only shows when debug is enabled");
```

CMake:

```cmake
find_package(spdlog REQUIRED)

add_executable(app src/main.cpp)
target_link_libraries(app spdlog::spdlog)
```

Hvis `find_package` ikke virker, kan det være fordi spdlog ikke er installeret som CMake package på systemet.

Log til fil:

```cpp
#include <spdlog/sinks/basic_file_sink.h>

int main() {
    auto logger = spdlog::basic_logger_mt("file_logger", "program.log");
    logger->info("Program started");
    logger->warn("Something looks wrong");
}
```

God brug i MQTT:

```cpp
spdlog::info("Connecting to {}", serverURI);
spdlog::info("Publishing to topic '{}'", TOPIC);
spdlog::error("MQTT error: {}", exc.what());
```

Eksamensting:

Logging gør det nemmere at forstå program flow uden at debugge linje for linje.
