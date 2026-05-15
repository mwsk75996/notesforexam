# DHCP, DNS og NAT

## DHCP

DHCP giver automatisk IP-konfiguration til klienter.

Klienten får typisk:

- IP-adresse
- subnetmask
- default gateway
- DNS-server

DHCP DORA:

```text
Discover -> Offer -> Request -> Acknowledge
```

Forklaring:

- Discover: klienten spørger efter en DHCP-server
- Offer: serveren tilbyder en IP
- Request: klienten beder om at bruge den IP
- ACK: serveren bekræfter leasen

DHCP bruger UDP:

```text
Client port: 68/UDP
Server port: 67/UDP
```

Wireshark filter:

```text
dhcp
bootp
udp.port == 67 || udp.port == 68
```

APIPA:

```text
169.254.0.0/16
```

Hvis en klient ikke får DHCP lease, kan den selv vælge en APIPA-adresse. To APIPA-enheder på samme link kan ofte kommunikere med hinanden, men de har normalt ikke gateway/internet.

## DNS

DNS oversætter navne til IP-adresser.

Eksempel:

```text
awesome.dk -> 192.168.x.x
dr.dk -> offentlig IP
```

DNS bruger typisk:

```text
UDP port 53
TCP port 53 ved større svar/zone transfers
```

Commands:

```sh
dig awesome.dk
nslookup awesome.dk
```

Spørg en bestemt DNS-server:

```sh
dig @192.168.10.10 awesome.dk
nslookup awesome.dk 192.168.10.10
```

Wireshark filter:

```text
dns
udp.port == 53
tcp.port == 53
```

`dnsmasq` kan bruges som simpel DNS/DHCP server.

Verbose mode betyder at serveren printer/logfører mere information om requests, så man kan se hvilke opslag klienterne laver.

## NAT

NAT står for Network Address Translation.

Source NAT bruges typisk når interne private IP'er skal ud på internettet.

Eksempel:

```text
192.168.12.12 -> NAT -> ekstern/router IP
```

Klienten tror den sender til internettet, men routeren oversætter source IP så returtrafikken kan finde tilbage.

Test NAT:

```sh
ping 8.8.8.8 -c 3
ping dr.dk -c 3
traceroute dr.dk
```

Hvis `ping 8.8.8.8` virker men `ping dr.dk` fejler, er det ofte DNS-problem.

Hvis gateway virker, men internet ikke virker, tjek:

- default route på klient
- default route på router
- NAT-regel
- security policy
- DNS

God eksamensforklaring:

NAT gør at flere private hosts kan dele én ekstern IP-adresse. Routeren holder styr på forbindelserne i en translation/session table.

