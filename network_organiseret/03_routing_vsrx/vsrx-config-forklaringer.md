# vSRX config forklaringer

Disse eksempler er baseret på mine GitHub repos:

- [ass6network](https://github.com/mwsk75996/ass6network) - NAT, zones, policies
- [ass18network](https://github.com/mwsk75996/ass18network) - DHCP local server, legacy DHCP, DHCP relay
- [ass32network](https://github.com/mwsk75996/ass32network) - Source NAT på fysisk SRX
- [ass42network](https://github.com/mwsk75996/ass42network) - DNS/DHCP/NAT samlet setup
- [ass54network](https://github.com/mwsk75996/ass54network) - address-book, zones og security policies

Jeg har fjernet passwords/secrets fra eksemplerne.

## Grundform

Typisk rækkefølge:

```text
configure
set interfaces ...
set routing-options ...
set security zones ...
set security policies ...
commit check
commit
```

Tjek bagefter:

```text
show interfaces terse
show route
show configuration routing-options
show security zones
show security policies
show security nat source
```

## Interface IP

Eksempel fra flere opgaver:

```text
set interfaces ge-0/0/1 unit 0 family inet address 192.168.10.1/24
set interfaces ge-0/0/2 unit 0 family inet address 192.168.11.1/24
set interfaces ge-0/0/3 unit 0 family inet address 10.10.10.1/24
```

God forklaring:

`ge-0/0/1.0` er logical unit 0 på interface `ge-0/0/1`. IP-adressen på routerens interface bliver typisk default gateway for subnettet.

## Default route

Bruges når routeren skal sende alt ukendt videre til upstream gateway.

```text
set routing-options static route 0.0.0.0/0 next-hop 10.56.16.1
```

Eller i ass6:

```text
set routing-options static route 0.0.0.0/0 next-hop 192.168.100.2
```

God forklaring:

`0.0.0.0/0` matcher alt trafik der ikke har en mere specifik rute.

## Static routes mellem to routere

Hvis R1 har `192.168.10.0/24` og `192.168.11.0/24`, og R2 har `192.168.12.0/24` og `192.168.13.0/24`.

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

God forklaring:

Routeren skal kende de remote subnets. Next-hop er den anden router på transit-netværket.

## Simpel trust zone

Brugt i flere opgaver hvor alt ligger i samme zone for at fokusere på routing.

```text
set security zones security-zone trust interfaces ge-0/0/1.0 host-inbound-traffic system-services ping
set security zones security-zone trust interfaces ge-0/0/1.0 host-inbound-traffic system-services ssh
set security zones security-zone trust interfaces ge-0/0/2.0 host-inbound-traffic system-services ping
set security zones security-zone trust interfaces ge-0/0/2.0 host-inbound-traffic system-services ssh
```

Hvis DHCP skal kunne modtages på interfacet:

```text
set security zones security-zone trust interfaces ge-0/0/1.0 host-inbound-traffic system-services dhcp
```

Simpel permit policy trust til trust:

```text
set security policies from-zone trust to-zone trust policy default-permit match source-address any
set security policies from-zone trust to-zone trust policy default-permit match destination-address any
set security policies from-zone trust to-zone trust policy default-permit match application any
set security policies from-zone trust to-zone trust policy default-permit then permit
```

God forklaring:

På SRX er routing ikke nok. Trafikken skal også tillades af security policy.

## Source NAT

Brugt i ass6, ass32 og ass42.

Typisk setup:

```text
set security nat source rule-set trust-to-untrust from zone trust
set security nat source rule-set trust-to-untrust to zone untrust
set security nat source rule-set trust-to-untrust rule rule-any-to-any match source-address 0.0.0.0/0
set security nat source rule-set trust-to-untrust rule rule-any-to-any match destination-address 0.0.0.0/0
set security nat source rule-set trust-to-untrust rule rule-any-to-any then source-nat interface
```

Tillad trust ud mod untrust:

```text
set security policies from-zone trust to-zone untrust policy internet-access match source-address any
set security policies from-zone trust to-zone untrust policy internet-access match destination-address any
set security policies from-zone trust to-zone untrust policy internet-access match application any
set security policies from-zone trust to-zone untrust policy internet-access then permit
```

Eksempel med trust og untrust interfaces:

```text
set security zones security-zone trust interfaces ge-0/0/1.0 host-inbound-traffic system-services ping
set security zones security-zone trust interfaces ge-0/0/3.0 host-inbound-traffic system-services ping
set security zones security-zone untrust interfaces ge-0/0/5.0 host-inbound-traffic system-services ping
```

God forklaring:

`source-nat interface` betyder at interne klienters source IP bliver oversat til routerens udgående interface-IP. Det er sådan private IP'er kan nå internettet.

## NAT med flere interne zones

Fra ass6-ideen med `IoT-Net1`, `IoT-Net2` og `WAN`:

```text
set security nat source rule-set nat-out from zone IoT-Net1
set security nat source rule-set nat-out from zone IoT-Net2
set security nat source rule-set nat-out to zone WAN
set security nat source rule-set nat-out rule r1 match source-address 0.0.0.0/0
set security nat source rule-set nat-out rule r1 then source-nat interface
```

Policies ud:

```text
set security policies from-zone IoT-Net1 to-zone WAN policy allow-out match source-address any
set security policies from-zone IoT-Net1 to-zone WAN policy allow-out match destination-address any
set security policies from-zone IoT-Net1 to-zone WAN policy allow-out match application any
set security policies from-zone IoT-Net1 to-zone WAN policy allow-out then permit
```

Samme pattern gentages for `IoT-Net2`.

## Extended DHCP local server

Fra ass18 og ass42.

Aktiver DHCP local server på interface:

```text
set system services dhcp-local-server group Net1 interface ge-0/0/1.0
set system services dhcp-local-server group Net2 interface ge-0/0/2.0
```

DHCP pool:

```text
set access address-assignment pool Net1 family inet network 192.168.1.0/24
set access address-assignment pool Net1 family inet range USERS low 192.168.1.10
set access address-assignment pool Net1 family inet range USERS high 192.168.1.100
set access address-assignment pool Net1 family inet dhcp-attributes maximum-lease-time 86400
set access address-assignment pool Net1 family inet dhcp-attributes name-server 8.8.8.8
set access address-assignment pool Net1 family inet dhcp-attributes router 192.168.1.1
```

Husk host-inbound:

```text
set security zones security-zone trust interfaces ge-0/0/1.0 host-inbound-traffic system-services dhcp
```

God forklaring:

`dhcp-local-server` siger hvilke interfaces der skal svare på DHCP. `access address-assignment pool` definerer hvilke IP'er, gateway og DNS klienterne får.

## Legacy DHCP

Fra ass18 R2 part 1:

```text
set system services dhcp pool 192.168.3.0/24 address-range low 192.168.3.10 high 192.168.3.100
set system services dhcp pool 192.168.3.0/24 name-server 8.8.8.8
set system services dhcp pool 192.168.3.0/24 router 192.168.3.1
set system services dhcp pool 192.168.3.0/24 default-lease-time 86400
```

God forklaring:

Legacy DHCP virker i ældre Junos-stil. Extended DHCP med `dhcp-local-server` og `access address-assignment` er den nyere/renere stil.

## DHCP relay

Fra ass18 part 2.

R2 relayer DHCP requests fra Net3/Net4 til R1:

```text
set forwarding-options helpers bootp server 10.10.10.10
set forwarding-options helpers bootp interface ge-0/0/1
set forwarding-options helpers bootp interface ge-0/0/2
```

På R1 skal DHCP-serveren også acceptere relay-trafik på transit-interface:

```text
set system services dhcp-local-server group Relay interface ge-0/0/3.0
```

Og R1 skal have pools for de remote netværk:

```text
set access address-assignment pool Net3 family inet network 192.168.3.0/24
set access address-assignment pool Net3 family inet range USERS low 192.168.3.10
set access address-assignment pool Net3 family inet range USERS high 192.168.3.100
set access address-assignment pool Net3 family inet dhcp-attributes router 192.168.3.1
```

God forklaring:

DHCP bruger broadcast, og broadcast bliver normalt ikke routet. DHCP relay løser det ved at routeren videresender klientens DHCP request til en DHCP-server på et andet subnet.

## DNS + DHCP + NAT samlet

Fra ass42.

DHCP giver klienterne intern DNS-server:

```text
set access address-assignment pool USERLAN-POOL family inet network 192.168.13.0/24
set access address-assignment pool USERLAN-POOL family inet range USERLAN-RANGE low 192.168.13.100
set access address-assignment pool USERLAN-POOL family inet range USERLAN-RANGE high 192.168.13.200
set access address-assignment pool USERLAN-POOL family inet dhcp-attributes name-server 192.168.11.5
set access address-assignment pool USERLAN-POOL family inet dhcp-attributes router 192.168.13.1
```

Host-inbound på trust interfaces tillader DNS:

```text
set security zones security-zone trust interfaces ge-0/0/1.0 host-inbound-traffic system-services dns
set security zones security-zone trust interfaces ge-0/0/2.0 host-inbound-traffic system-services dns
set security zones security-zone trust interfaces ge-0/0/3.0 host-inbound-traffic system-services dns
```

God forklaring:

Klienter på USERLAN får DNS-serveren `192.168.11.5` via DHCP. Når de laver DNS-opslag, sendes forespørgslen til den interne DNS-server i stedet for fx `8.8.8.8`.

## Address book

Fra ass54.

Address book gør policies nemmere at læse:

```text
set security address-book global address SENSOR_LAN 192.168.10.0/24
set security address-book global address SERVER_LAN 192.168.11.0/24
set security address-book global address WEB_SERVER 192.168.11.2/32
set security address-book global address PC1 192.168.10.2/32
set security address-book global address PC4 192.168.13.2/32
set security address-book global address INTER_LAN 10.10.10.0/24
```

God forklaring:

I stedet for at skrive IP-adresser direkte i policies, giver man dem navne. Det gør security policies mere læsbare.

## Custom application på port 8000

Fra ass54 og ass6.

```text
set applications application my-http-8000 application-protocol http
set applications application my-http-8000 protocol tcp
set applications application my-http-8000 destination-port 8000
```

Brug i policy:

```text
set security policies from-zone SENSOR_LAN to-zone SERVER_LAN policy allow-http match application my-http-8000
```

God forklaring:

Hvis en webserver kører på port 8000 i stedet for standard HTTP port 80, kan man lave en custom application og bruge den i policies.

## Single zone policy med specifikke hosts

Fra ass54 single-zone.

```text
set security policies from-zone myTrust_1 to-zone myTrust_1 policy allow-pc1-pc2-icmp-to-any match source-address PC1
set security policies from-zone myTrust_1 to-zone myTrust_1 policy allow-pc1-pc2-icmp-to-any match source-address PC2
set security policies from-zone myTrust_1 to-zone myTrust_1 policy allow-pc1-pc2-icmp-to-any match destination-address any
set security policies from-zone myTrust_1 to-zone myTrust_1 policy allow-pc1-pc2-icmp-to-any match application junos-icmp-ping
set security policies from-zone myTrust_1 to-zone myTrust_1 policy allow-pc1-pc2-icmp-to-any then permit
```

Default deny:

```text
set security policies default-policy deny-all
```

God forklaring:

Selv når alt ligger i samme zone, kan man stadig lave specifikke policies og slutte med `default-policy deny-all`, så kun det ønskede trafikmønster virker.

## Multi-zone eksempel

Fra ass54 multizone.

Zones:

```text
set security zones security-zone SENSOR_LAN interfaces ge-0/0/1.0 host-inbound-traffic system-services ping
set security zones security-zone SENSOR_LAN interfaces ge-0/0/1.0 host-inbound-traffic system-services traceroute

set security zones security-zone SERVER_LAN interfaces ge-0/0/2.0 host-inbound-traffic system-services ping
set security zones security-zone SERVER_LAN interfaces ge-0/0/2.0 host-inbound-traffic system-services traceroute

set security zones security-zone INTER_LAN_1 interfaces ge-0/0/3.0 host-inbound-traffic system-services ping
set security zones security-zone INTER_LAN_1 interfaces ge-0/0/3.0 host-inbound-traffic system-services traceroute
```

Policy fra sensor til server:

```text
set security policies from-zone SENSOR_LAN to-zone SERVER_LAN policy allow-pc1-to-server-lan match source-address any
set security policies from-zone SENSOR_LAN to-zone SERVER_LAN policy allow-pc1-to-server-lan match destination-address any
set security policies from-zone SENSOR_LAN to-zone SERVER_LAN policy allow-pc1-to-server-lan match application junos-icmp-ping
set security policies from-zone SENSOR_LAN to-zone SERVER_LAN policy allow-pc1-to-server-lan match application my-http-8000
set security policies from-zone SENSOR_LAN to-zone SERVER_LAN policy allow-pc1-to-server-lan then permit
```

God forklaring:

Multi-zone design er mere realistisk, fordi hvert subnet får sin egen zone. Så kan man styre præcist hvilken trafik der må gå mellem zonerne.

## Fejlfinding

Hvis ping ikke virker:

```text
show interfaces terse
show route
show security zones
show security policies
show configuration routing-options
```

Tjek:

- Har interface den rigtige IP?
- Er interfacet i en zone?
- Tillader `host-inbound-traffic` ping til routeren?
- Findes der route til destinationen?
- Findes der policy mellem source-zone og destination-zone?
- Hvis internet: findes default route og NAT?
- Hvis DHCP: er `dhcp` tilladt i host-inbound på client interface?

God eksamenssætning:

På SRX skal tre ting passe samtidig: interface/routing, zones/policies og eventuelt NAT/service config.
