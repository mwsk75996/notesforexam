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

## Headers og source files

En header (`.hpp`) beskriver hvad andre filer må bruge.

En source file (`.cpp`) indeholder selve implementeringen.

Typisk opdeling:

```text
helper.hpp  -> declarations: hvad findes der?
helper.cpp  -> definitions: hvordan virker det?
main.cpp    -> bruger funktionerne/classes fra headeren
```

En declaration fortæller compileren at noget findes:

```cpp
// helper.hpp
#pragma once

int add(int a, int b);
```

En definition indeholder koden:

```cpp
// helper.cpp
#include "helper.hpp"

int add(int a, int b) {
    return a + b;
}
```

Når `main.cpp` inkluderer headeren, kender den funktionen uden at kende hele implementeringen:

```cpp
// main.cpp
#include <iostream>

#include "helper.hpp"

int main() {
    std::cout << add(2, 3) << "\n";
}
```

Derfor skal `helper.cpp` stadig med i compile/link:

```sh
g++ -std=c++17 main.cpp helper.cpp -o app
```

Hvis du kun compiler `main.cpp`, kan compileren godt forstå kaldet til `add`, men linkeren kan ikke finde selve funktionen. Det giver typisk `undefined reference to add`.

Hvorfor ikke bare skrive alt i `.hpp`?

- `.hpp` bliver kopieret ind i hver `.cpp` fil der inkluderer den.
- Hvis almindelige funktioner/classes implementeres direkte i headeren, kan man nemt få duplicate definitions.
- Store implementeringer i headers gør compile langsommere, fordi mange filer skal gencompiles når headeren ændres.
- `.cpp` skjuler implementation details og gør projektet nemmere at overskue.

Hvornår giver kode i headers mening?

- små `inline` funktioner
- templates, fordi compileren ofte skal se hele implementationen
- små structs/classes hvor alt er meget simpelt

Hvis headers ligger i en `include/` mappe:

```sh
g++ -std=c++17 -Iinclude src/main.cpp -o app
```

Typiske fejl:

`undefined reference to ...`

Betyder ofte at en `.cpp` fil eller et library mangler at blive linket.

`No such file or directory`

Betyder ofte at en `#include` sti er forkert, eller at `-I...` mangler.

`permission denied` når du kører et script:

```sh
chmod +x ./run.sh
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
