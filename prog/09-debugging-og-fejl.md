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
target_compile_options(app PUBLIC -Wall -Wextra -Wfloat-conversion)
```

Typiske C++ fejl:

`undefined reference`

Linker fejl. Mangler ofte en `.cpp` fil eller et library i `target_link_libraries`.

`No such file or directory`

Include path eller filnavn er forkert.

`segmentation fault`

Programmet bruger memory forkert. Typisk null pointer, out of bounds, eller objekt der ikke findes længere.

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

