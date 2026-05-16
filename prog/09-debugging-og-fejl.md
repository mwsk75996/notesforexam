# Debugging og typiske fejl

Når noget ikke virker, start simpelt.

Tjek hvor du står:

```sh
pwd
ls
```

Tjek om filen findes:

```sh
ls src
ls build
```

Slet build og byg igen:

```sh
rm -rf build
cmake -S . -B build
cmake --build build
```

Compiler warnings er nyttige:

```cmake
target_compile_options(app PRIVATE -Wall -Wextra -Wfloat-conversion)
```

Debug build er bedre når man skal finde fejl:

```sh
cmake -S . -B build -DCMAKE_BUILD_TYPE=Debug
cmake --build build
```

AddressSanitizer kan finde mange memory-fejl:

```cmake
target_compile_options(app PRIVATE -fsanitize=address -g)
target_link_options(app PRIVATE -fsanitize=address)
```

Typiske C++ fejl:

`undefined reference`

Linker fejl. Mangler ofte en `.cpp` fil eller et library i `target_link_libraries`.

`No such file or directory`

Include path eller filnavn er forkert.

`segmentation fault`

Programmet bruger memory forkert. Typisk null pointer, out of bounds, eller objekt der ikke findes længere.

Kør med gdb og få backtrace:

```sh
gdb ./build/app
run
bt
```

`permission denied`

Script eller program mangler execute permission:

```sh
chmod +x run.sh
```

MQTT fejl:

- Broker kører ikke
- Forkert topic
- Forkert port
- Subscriber startes efter publisher
- Client ID konflikter

Gode små debug prints:

```cpp
std::cout << "value = " << value << "\n";
```

Eller med spdlog:

```cpp
spdlog::debug("value = {}", value);
```

Hvis programmet aldrig kommer forbi et punkt, sæt prints omkring det:

```cpp
std::cout << "before connect\n";
client.connect()->wait();
std::cout << "after connect\n";
```
