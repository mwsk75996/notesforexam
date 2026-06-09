# Encryption

Encryption betyder at data gøres ulæseligt, men kan gøres læseligt igen med en key.

Kort forskel:

- Hashing: one-way
- Encryption: two-way

Symmetric encryption:

Samme key bruges til encrypt og decrypt.

```text
plaintext + key -> ciphertext
ciphertext + same key -> plaintext
```

Asymmetric encryption:

Der er en public key og en private key.

- Public key kan deles
- Private key skal holdes hemmelig

Bruges ofte til TLS/HTTPS, login, certificates og key exchange.

Kort ide:

```text
public key  -> må deles med andre
private key -> skal kun ejes af dig/serveren
```

I praksis bruges asymmetric encryption ofte til at udveksle en symmetric key eller til signatures. Man krypterer normalt ikke store filer direkte med RSA.

Gode ord:

- plaintext: original læsbar tekst
- ciphertext: krypteret tekst
- key: hemmelig nøgle
- IV/nonce: ekstra random værdi så samme tekst ikke altid giver samme output
- decrypt: gøre ciphertext læsbart igen

Simpel OpenSSL command til fil med password:

```sh
openssl enc -aes-256-cbc -salt -pbkdf2 -iter 100000 -in secret.txt -out secret.txt.enc
```

Decrypt igen:

```sh
openssl enc -d -aes-256-cbc -pbkdf2 -iter 100000 -in secret.txt.enc -out secret.txt
```

`-pbkdf2` gør passwordet til en stærkere key-derivation i stedet for en gammel svagere standard.

Til moderne kode bør man helst bruge et library og en authenticated mode som AES-GCM eller ChaCha20-Poly1305.

## Public/private keys i C++ med OpenSSL

Eksempel der laver et RSA keypair og gemmer det i to filer:

```cpp
#include <cstdio>
#include <iostream>

#include <openssl/evp.h>
#include <openssl/pem.h>

int main() {
    EVP_PKEY* keyPair = EVP_RSA_gen(2048);
    if (keyPair == nullptr) {
        std::cerr << "Could not generate key pair\n";
        return 1;
    }

    FILE* privateFile = std::fopen("private_key.pem", "wb");
    if (privateFile == nullptr) {
        std::cerr << "Could not open private_key.pem\n";
        EVP_PKEY_free(keyPair);
        return 1;
    }

    PEM_write_PrivateKey(privateFile, keyPair, nullptr, nullptr, 0, nullptr, nullptr);
    std::fclose(privateFile);

    FILE* publicFile = std::fopen("public_key.pem", "wb");
    if (publicFile == nullptr) {
        std::cerr << "Could not open public_key.pem\n";
        EVP_PKEY_free(keyPair);
        return 1;
    }

    PEM_write_PUBKEY(publicFile, keyPair);
    std::fclose(publicFile);

    EVP_PKEY_free(keyPair);

    std::cout << "Created private_key.pem and public_key.pem\n";
}
```

Kompilér:

```sh
g++ -std=c++17 keygen.cpp -o keygen -lcrypto
```

Efter kørsel:

```text
private_key.pem  -> hemmelig key, må ikke deles
public_key.pem   -> public key, kan deles
```

Samme ide med OpenSSL i terminalen:

```sh
openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:2048 -out private_key.pem
openssl pkey -in private_key.pem -pubout -out public_key.pem
```

## libsodium encryption demo

Repo-eksempel:

- [libsodium-cryptography-demo](https://github.com/mwsk75996/libsodium-cryptography-demo)

libsodium har højere-level crypto APIs end rå OpenSSL. I repoet bliver en MAC-adresse krypteret på to måder:

```text
crypto_secretbox_easy -> symmetrisk encryption med samme secret key
crypto_box_seal      -> asymmetrisk encryption med public/private keypair
```

Symmetrisk ide:

```cpp
std::array<unsigned char, crypto_secretbox_KEYBYTES> key{};
std::array<unsigned char, crypto_secretbox_NONCEBYTES> nonce{};

randombytes_buf(key.data(), key.size());
randombytes_buf(nonce.data(), nonce.size());

crypto_secretbox_easy(
    ciphertext.data(),
    message,
    messageSize,
    nonce.data(),
    key.data()
);
```

Asymmetrisk ide:

```cpp
std::array<unsigned char, crypto_box_PUBLICKEYBYTES> publicKey{};
std::array<unsigned char, crypto_box_SECRETKEYBYTES> secretKey{};

crypto_box_keypair(publicKey.data(), secretKey.data());

crypto_box_seal(
    ciphertext.data(),
    message,
    messageSize,
    publicKey.data()
);
```

God eksamensforklaring:

Symmetrisk encryption er hurtig, men begge parter skal kende samme key. Asymmetrisk encryption gør det muligt at kryptere med en public key, mens kun private key kan dekryptere.

Hvad encryption beskytter:

```text
secret.txt      -> læsbart indhold
secret.txt.enc  -> krypteret indhold
password/key    -> bruges til at åbne igen
```

Vigtigt:

- Lav ikke din egen encryption algorithm.
- Genbrug ikke nonce/IV forkert.
- Gem aldrig keys direkte i source code.
- Hashing er ikke encryption.
- Encryption skjuler indhold, men fortæller ikke alene om data er ændret. Brug authenticated encryption eller MAC/signature for integritet.

God eksamensforklaring:

Encryption bruges når data skal kunne læses igen af en person eller et system med den rigtige key. Hashing bruges når man kun skal kunne verificere at input matcher.
