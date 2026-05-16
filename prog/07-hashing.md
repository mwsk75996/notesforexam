# Hashing

Hashing laver data om til et fast fingerprint.

Vigtigt: hashing er ikke encryption. Man kan normalt ikke gå tilbage fra hash til original tekst.

Bruges til:

- checke om data er ændret
- gemme passwords på en sikrere måde
- sammenligne store data uden at sammenligne alt
- lave checksums

Eksempel ide:

```text
"hello" -> hash function -> "2cf24dba..."
```

Samme input giver samme hash.

Lille ændring giver helt anden hash.

Hashing i terminal med SHA-256:

```sh
echo -n "hello" | sha256sum
```

Hash en fil:

```sh
sha256sum file.txt
```

Check om to filer er ens:

```sh
sha256sum file1.txt file2.txt
```

C++ standard library har `std::hash`, men den er ikke til sikkerhed:

```cpp
#include <functional>
#include <iostream>
#include <string>

int main() {
    std::string text = "hello";
    std::size_t value = std::hash<std::string>{}(text);

    std::cout << value << "\n";
}
```

Vigtigt om `std::hash`:

- fint til hash maps og simple øvelser
- ikke cryptographic secure
- brug ikke til passwords eller sikkerhed

Til sikker hashing bruger man typisk SHA-256, bcrypt, Argon2 eller lignende. Passwords bør ikke bare hashes med SHA-256 alene; de skal også have salt og en password hashing algoritme.

God eksamensforklaring:

Hashing er one-way. Encryption er two-way med en key. Derfor kan man verificere et password ved at hashe input og sammenligne med gemt hash, uden at kende original password.

Eksempel med SHA-256 i C++ med OpenSSL:

```cpp
#include <iostream>
#include <string>
#include <openssl/sha.h>
#include <iomanip>
#include <sstream>

int main() {
    std::string text = "hemmeligt";
    unsigned char hash[SHA256_DIGEST_LENGTH];

    SHA256((unsigned char*)text.c_str(), text.size(), hash);

    std::stringstream ss;
    for (int i = 0; i < SHA256_DIGEST_LENGTH; i++) {
        ss << std::hex << std::setw(2) << std::setfill('0') << (int)hash[i];
    }

    std::cout << ss.str() << "\n";
}
```

Kompilér med: `g++ sha256.cpp -o sha256 -lssl -lcrypto`

SHA-256 giver altid samme hash for samme input. Hurtigt, men ikke nok til passwords alene.

Eksempel med bcrypt i C++:

```cpp
#include <iostream>
#include <string>
#include <bcrypt/BCrypt.hpp>

int main() {
    std::string password = "hemmeligt";

    // Generer salt og hash
    std::string hashed = BCrypt::generateHash(password);

    std::cout << hashed << "\n";

    // Tjek password
    if (BCrypt::validatePassword(password, hashed)) {
        std::cout << "OK\n";
    }
}
```

bcrypt er lavet til passwords. Det bruger salt og er langsomt, så det er sværere at brute-force.

Installation og docs:

SHA-256 via OpenSSL:

- Docs: https://docs.openssl.org/3.1/man3/SHA256_Init/
- Debian: `sudo apt install libssl-dev`
- Arch: `sudo pacman -S openssl`
- Windows (vcpkg): `vcpkg install openssl`
- Windows (manuel): Download fra https://openssl-library.org/source/ og build med CMake/Perl

bcrypt via libbcrypt (trusch/libbcrypt):

- Docs: https://github.com/trusch/libbcrypt
- Debian/Arch: byg fra source:
  ```sh
  git clone https://github.com/trusch/libbcrypt
  cd libbcrypt
  mkdir build && cd build
  cmake ..
  make
  sudo make install
  sudo ldconfig
  ```
- Windows: kræver CMake og en C++ compiler (MSVC eller MinGW). Byg fra source som ovenfor, eller brug Windows egen BCrypt API (`bcrypt.h` + `#pragma comment(lib, "bcrypt")`)
- Windows (vcpkg): `vcpkg install libxcrypt` (understøtter bcrypt hashing)

