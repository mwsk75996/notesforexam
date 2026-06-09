# Eksamens Netværksforberedelse - Cheatsheet

Dette cheatsheet er udarbejdet direkte på baggrund af kravene i **`ITT2_eksamen_studerende_forberedelse 2026.pdf`**.
Dokumentet beskriver opsætning, konfiguration og verifikation af eksamensnetværket (R1 vSRX router, PC3 og PC4 Xubuntu Linuxmaskiner).

---

## 1. Topologi og Netværksdiagram

Netværket er opsat i **VMware Workstation**:
```text
                    [ Internet (NAT/Bridge) ]
                                |
                                |
                       [ Interface: ge-0/0/0.0 ]
                                |
                         [ R1 (vSRX) ]
                         /           \
   [ Interface: ge-0/0/1.0 ]       [ Interface: ge-0/0/2.0 ]
               |                               |
        [ Subnet A ]                    [ Subnet B ]
               |                               |
       [ Xubuntu PC3 ]                  [ Xubuntu PC4 ]
  - static IP (eller static dhcp) -    - DHCP IP fra PC3 eller R1 -
  - Services: ssh, dnsmasq, nginx -     - Hostname: PC4 -
  - Hostname: PC3 -
```

---

## 2. R1: vSRX Firewall og Router Konfiguration

Hele konfigurationen foretages via Putty/SSH eller Seriel konsol.

### A. Interface Opsætning (Eksempel)
Indstil IP-adresser på routerens interfaces. Typisk er `ge-0/0/0` WAN-interfacet (mod internettet via VMware NAT), mens `ge-0/0/1` og `ge-0/0/2` er LAN-interfaces mod hhv. PC3 og PC4.
```text
configure
set interfaces ge-0/0/0 unit 0 family inet address 192.168.100.10/24  # WAN IP
set interfaces ge-0/0/1 unit 0 family inet address 192.168.10.1/24   # Gateway for PC3
set interfaces ge-0/0/2 unit 0 family inet address 192.168.20.1/24   # Gateway for PC4
```

### B. Routing-Options (Default Gateway til Internet)
Routeren skal kunne videresende alt ukendt trafik ud mod internettet via VMware Workstations standard gateway (f.eks. `.2` eller `.1` på VMware NAT netværket):
```text
set routing-options static route 0.0.0.0/0 next-hop 192.168.100.2
```

### C. Security Zones
På en SRX skal interfaces placeres i sikkerhedszoner. Vi opretter typisk en `trust` zone til LAN og en `untrust` zone til WAN.

#### Placer interfaces:
```text
set security zones security-zone trust interfaces ge-0/0/1.0
set security zones security-zone trust interfaces ge-0/0/2.0
set security zones security-zone untrust interfaces ge-0/0/0.0
```

#### Tillad system-services på interfaces (så enheder kan pinge routeren):
```text
set security zones security-zone trust interfaces ge-0/0/1.0 host-inbound-traffic system-services ping
set security zones security-zone trust interfaces ge-0/0/1.0 host-inbound-traffic system-services ssh
set security zones security-zone trust interfaces ge-0/0/2.0 host-inbound-traffic system-services ping
set security zones security-zone untrust interfaces ge-0/0/0.0 host-inbound-traffic system-services ping
```

### D. Security Policies
Zoneregler bestemmer, hvilken trafik der må passere routeren.

#### Tillad alt LAN-til-LAN (Trust til Trust):
```text
set security policies from-zone trust to-zone trust policy local-permit match source-address any
set security policies from-zone trust to-zone trust policy local-permit match destination-address any
set security policies from-zone trust to-zone trust policy local-permit match application any
set security policies from-zone trust to-zone trust policy local-permit then permit
```

#### Tillad LAN-til-Internet (Trust til Untrust):
```text
set security policies from-zone trust to-zone untrust policy internet-access match source-address any
set security policies from-zone trust to-zone untrust policy internet-access match destination-address any
set security policies from-zone trust to-zone untrust policy internet-access match application any
set security policies from-zone trust to-zone untrust policy internet-access then permit
```

### E. Source NAT (så PC3 og PC4 kan nå internettet)
Da PC3 og PC4 bruger private IP-adresser, skal routeren oversætte deres kilde-IP (Source IP) til sin egen offentlige/eksterne IP på WAN-interfacet:
```text
set security nat source rule-set trust-to-untrust from zone trust
set security nat source rule-set trust-to-untrust to zone untrust
set security nat source rule-set trust-to-untrust rule any-to-internet match source-address 0.0.0.0/0
set security nat source rule-set trust-to-untrust rule any-to-internet match destination-address 0.0.0.0/0
set security nat source rule-set trust-to-untrust rule any-to-internet then source-nat interface
```

### F. Gem og Verificer på R1
```text
commit check
commit

# Test-kommandoer:
show interfaces terse
show route
show security zones
show security policies
show security nat source rule all
```

---

## 3. PC3: Xubuntu Konfiguration

PC3 fungerer som den centrale Linux-server i testopstillingen.

### A. Hostname Konfiguration
Navnet skal ændres, så det fremgår direkte i prompten:
```sh
# Ændr hostname permanent
sudo hostnamectl set-hostname PC3

# Rediger hosts filen for at undgå sudo-advarsler
sudo nano /etc/hosts
```
*I `/etc/hosts` skal linjen for localhost tilpasses:*
```text
127.0.0.1   localhost PC3
```
*Genstart terminalen for at se ændringen i prompten (`bruger@PC3:~$`).*

### B. OpenSSH Server (Fjernadgang)
```sh
# Installer server
sudo apt install openssh-server -y

# Start og enable servicen
sudo systemctl enable --now ssh

# Tjek status
sudo systemctl status ssh
```

### C. Nginx Webserver
```sh
# Installer
sudo apt install nginx -y

# Start og enable servicen
sudo systemctl enable --now nginx

# Opret en simpel test-hjemmeside
sudo mkdir -p /var/www/html
echo "<h1>PC3 Nginx Webserver - Eksamensforberedelse</h1>" | sudo tee /var/www/html/index.html

# Tjek at nginx kører og lytter på port 80
sudo ss -tulpn | grep ':80'
```

### D. Dnsmasq (DHCP & DNS Server)
Dnsmasq installeres på PC3 for at kunne tildele IP-adresser til PC4 samt fungere som lokal DNS.

```sh
# Deaktiver systemd-resolved hvis det konflikter med dnsmasq på port 53
sudo systemctl stop systemd-resolved
sudo systemctl disable systemd-resolved

# Installer dnsmasq
sudo apt install dnsmasq -y
```

#### Rediger konfigurationsfilen `/etc/dnsmasq.conf`:
```sh
sudo nano /etc/dnsmasq.conf
```
*Tilføj eller tilpas følgende konfiguration:*
```ini
# Lyt kun på det interface, der vender mod det lokale netværk (f.eks. ens33)
interface=ens33

# DNS indstillinger
domain-needed
bogus-priv
verbose-dns    # Vigtigt: sikrer logning af forespørgsler til fejlfinding!

# DHCP indstillinger
dhcp-range=192.168.20.50,192.168.20.150,255.255.255.0,12h
dhcp-option=option:router,192.168.20.1              # PC4's gateway (R1 interface)
dhcp-option=option:dns-server,192.168.10.10,8.8.8.8 # DNS servere til PC4

# Statisk DHCP lease til PC4 (hvis du vil låse dens IP ud fra MAC)
# dhcp-host=11:22:33:44:55:66,192.168.20.100,PC4
```

Genstart dnsmasq:
```sh
sudo systemctl restart dnsmasq
sudo systemctl status dnsmasq
```

---

## 4. PC4: Xubuntu Konfiguration

PC4 fungerer som klienten.

### A. Hostname Konfiguration
```sh
sudo hostnamectl set-hostname PC4
sudo nano /etc/hosts
```
*Tilpas `/etc/hosts`:*
```text
127.0.0.1   localhost PC4
```

### B. Modtag IP-adresse via DHCP (fra PC3)
Sørg for, at PC4's netværksinterface er sat til at modtage IP automatisk.
```sh
# Forny IP-adresse via DHCP client
sudo dhclient -r && sudo dhclient ens33

# Tjek IP og gateway
ip a
ip route
```

---

## 5. Fejlfinding og Verifikation (Eksamens-Tjekliste)

Når netværket kører, skal du kunne udføre følgende tests for at bevise, at opsætningen er korrekt.

### I. Lag 3 Connectivity (Ping)
*   Fra **PC3**: Ping standard gateway (`192.168.10.1`) og PC4 (`192.168.20.x`).
*   Fra **PC4**: Ping standard gateway (`192.168.20.1`) og PC3 (`192.168.10.10`).
*   Begge maskiner skal kunne pinge eksterne IP'er (f.eks. `8.8.8.8`).
```sh
ping 8.8.8.8 -c 3
```

### II. DNS og Navneopløsning (dig / nslookup)
*   Test at DNS-opslag virker mod internettet:
```sh
dig dr.dk
nslookup google.com
```
*   Test opslag mod den lokale dnsmasq server på PC3:
```sh
dig @192.168.10.10 dr.dk
```

### III. Webserver Test (curl)
*   Hent PC3's hjemmeside fra PC4:
```sh
curl -I http://192.168.10.10
curl http://192.168.10.10
```

### IV. SSH Login
*   Forbind fra PC4 til PC3:
```sh
ssh bruger@192.168.10.10
```

### V. Wireshark Fejlsøgningsfiltre
Brug disse filtre i Wireshark på PC3/PC4 for at fange relevant eksamenstrafik:
*   **DHCP Handshake (DORA):** `bootp || dhcp` (Tjek Discover, Offer, Request, ACK).
*   **DNS opslag:** `dns || udp.port == 53` (Tjek queries og svar).
*   **HTTP trafik:** `http || tcp.port == 80` (Tjek GET requests og 200 OK responses).
*   **SSH forbindelser:** `ssh || tcp.port == 22` (Tjek Key Exchange og krypteret trafik).
