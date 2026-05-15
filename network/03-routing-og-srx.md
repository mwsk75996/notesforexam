# Routing og Juniper SRX

Routing bruges når trafik skal mellem forskellige subnets.

En host kigger først:

```text
Er destinationen i mit eget subnet?
```

Hvis ja: send direkte til destinationens MAC.

Hvis nej: send til default gateway.

## Linux routing

Se IP-adresser:

```sh
ip a
```

Se routing table:

```sh
ip route
```

Typisk default route:

```text
default via 192.168.1.1 dev eth0
```

Test rækkefølge:

```sh
ping <egen-gateway> -c 3
ping <host-i-andet-subnet> -c 3
traceroute <host-i-andet-subnet>
```

## Juniper SRX basis

Gå i config mode:

```text
configure
```

Sæt interface IP:

```text
set interfaces ge-0/0/1 unit 0 family inet address 192.168.10.1/24
```

Sæt statisk route:

```text
set routing-options static route 192.168.20.0/24 next-hop 10.10.10.2
```

Tillad ping ind på interface:

```text
set security zones security-zone myTrust interfaces ge-0/0/1.0 host-inbound-traffic system-services ping
```

Simpel permit policy:

```text
set security policies from-zone myTrust to-zone myTrust policy default-permit match source-address any
set security policies from-zone myTrust to-zone myTrust policy default-permit match destination-address any
set security policies from-zone myTrust to-zone myTrust policy default-permit match application any
set security policies from-zone myTrust to-zone myTrust policy default-permit then permit
```

Gem config:

```text
commit check
commit
```

Visning/fejlfinding:

```text
show interfaces terse
show route
show route protocol static
show configuration routing-options
show security zones
show security policies
```

## To routere med statisk routing

Hvis R1 har LAN1 og LAN2, og R2 har LAN3 og LAN4, skal de kende hinandens netværk.

På R1:

```text
set routing-options static route 192.168.12.0/24 next-hop 10.10.10.2
set routing-options static route 192.168.13.0/24 next-hop 10.10.10.2
```

På R2:

```text
set routing-options static route 192.168.10.0/24 next-hop 10.10.10.1
set routing-options static route 192.168.11.0/24 next-hop 10.10.10.1
```

## Wireshark forklaring ved routing

Når en pakke routes mellem subnets:

- IP source/destination bliver normalt den samme fra ende til ende.
- MAC source/destination ændres ved hvert hop.
- Routeren fjerner gammel Ethernet frame og laver en ny på næste interface.

God eksamenssætning:

Routere adskiller broadcast-domæner. ARP/broadcast fra ét subnet bliver ikke videresendt til et andet subnet.

