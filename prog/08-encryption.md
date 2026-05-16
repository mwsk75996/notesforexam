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
