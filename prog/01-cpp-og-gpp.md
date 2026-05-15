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

Hvis headers ligger i en `include/` mappe:

```sh
g++ -std=c++17 -Iinclude src/main.cpp -o app
```

Typiske fejl:

`undefined reference to ...`

Betyder ofte at en `.cpp` fil eller et library mangler at blive linket.

`No such file or directory`

Betyder ofte at en `#include` sti er forkert, eller at `-I...` mangler.

`permission denied` når du kører programmet:

```sh
chmod +x ./main
```

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

