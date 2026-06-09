# SSH (Secure Shell)

SSH bruges til krypteret fjernadgang (remote login) og sikker filoverførsel.

## Installation og opsætning af SSH Server

For at tillade andre enheder at logge på maskinen skal `openssh-server` installeres og startes.

### Installation (Debian/Ubuntu/Xubuntu):
```sh
sudo apt update
sudo apt install openssh-client openssh-server -y
```

### Styr SSH service (systemd):
```sh
# Aktivér ved opstart
sudo systemctl enable ssh

# Start servicen nu
sudo systemctl start ssh

# Tjek status
sudo systemctl status ssh
```

### Tillad SSH i den lokale firewall (UFW):
```sh
sudo ufw allow ssh
```

---

## Brug af SSH

### Log på en remote maskine:
```sh
ssh bruger@<ip-adresse>
```
*Eksempel:*
```sh
ssh karen@192.168.10.10
```

### Opret en ny bruger på serveren (til test/eksamen):
```sh
sudo adduser karen
```

---

## Nøgler og sikkerhed

Når en SSH-forbindelse etableres, udveksles krypteringsnøgler for at verificere serverens identitet og kryptere sessionen.

### Host Keys (Server-nøgler):
Serveren identificerer sig med sine egne unikke nøgler. Disse ligger typisk i:
```text
/etc/ssh/ssh_host_ed25519_key        (Privat nøgle - må ALDRIG deles)
/etc/ssh/ssh_host_ed25519_key.pub    (Offentlig nøgle)
```

### Known Hosts (Klient-verifikation):
Første gang du forbinder til en ny SSH-server fra en klient, spørger programmet om du accepterer serverens fingeraftryk.
Når du svarer ja, gemmes serverens offentlige nøgle i:
```text
~/.ssh/known_hosts
```
Dette forhindrer *Man-in-the-Middle* (MitM) angreb. Hvis serverens nøgle ændrer sig senere, vil SSH nægte at logge på og advare om en potentiel sikkerhedstrussel.

---

## Filoverførsel med SCP (Secure Copy)

Kopier en fil fra din lokale PC til en remote maskine:
```sh
scp <filnavn> bruger@<ip-adresse>:<sti-på-server>
```
*Eksempel (kopierer `test.txt` til karens hjemmemappe på 192.168.10.10):*
```sh
scp test.txt karen@192.168.10.10:/home/karen/
```

---

## Wireshark og Fejlfinding

### Nyttige display filters:
```text
ssh
tcp.port == 22
```

### God eksamensforklaring:
SSH kører på applikationslaget og etableres ovenpå en stabil TCP-forbindelse (port 22). Før login-prompter eller data sendes, laver SSH en handshake, hvor kryptering og server-identifikation (host keys) aftales. Derefter er alt indhold krypteret.
