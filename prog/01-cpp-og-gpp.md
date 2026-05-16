# C++ og g++

`g++` er C++ compileren. Den kan bruges direkte til små programmer uden CMake.

Simpel compile:

```sh
g++ main.cpp -o main
./main
```

Med C++17:

```sh
g++ -std=c++17 main.cpp -o main
```

Med warnings:

```sh
g++ -std=c++17 -Wall -Wextra main.cpp -o main
```

Hvis der er flere `.cpp` filer:

```sh
g++ -std=c++17 main.cpp helper.cpp -o app
```

Det er vigtigt at compile alle `.cpp` filer der indeholder kode. Headers (`.h`/`.hpp`) bliver normalt ikke compiled direkte; de bliver inkluderet af `.cpp` filer.

Hvis headers ligger i en `include/` mappe:

```sh
g++ -std=c++17 -Iinclude src/main.cpp -o app
```

Mini eksempel med header og cpp:

```cpp
// helper.hpp
#pragma once

int add(int a, int b);
```

```cpp
// helper.cpp
#include "helper.hpp"

int add(int a, int b) {
    return a + b;
}
```

```cpp
// main.cpp
#include <iostream>

#include "helper.hpp"

int main() {
    std::cout << add(2, 3) << "\n";
}
```

Compile:

```sh
g++ -std=c++17 -Wall -Wextra main.cpp helper.cpp -o app
```

Typiske fejl:

`undefined reference to ...`

Betyder ofte at en `.cpp` fil eller et library mangler at blive linket.

`No such file or directory`

Betyder ofte at en `#include` sti er forkert, eller at `-I...` mangler.

`permission denied` når du kører et script:

```sh
chmod +x ./run.sh
chmod +x ./main
```

Et program compiled med `g++ -o main` bliver normalt executable automatisk. `chmod +x` er mest relevant for `.sh` scripts.

Mini template:

```cpp
#include <iostream>
#include <string>

int main() {
    std::string name = "Mathias";
    std::cout << "Hej " << name << "\n";
    return 0;
}
```
