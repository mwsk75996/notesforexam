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

