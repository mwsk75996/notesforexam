# Netværk eksamen - overblik

De her noter er lavet ud fra opgaverne i `Netværks eksempler`.

De vigtigste emner der går igen:

- IP-adresser, binær og subnetting
- ARP, MAC-adresser og broadcast
- Switch, hub, bridge og STP
- Routing, default gateway og statiske routes
- Juniper SRX/vSRX konfiguration
- DHCP, DORA og APIPA
- DNS, dnsmasq, `dig` og `nslookup`
- Source NAT
- Security zones og policies på SRX
- Wireshark analyse
- MQTT, SSH og ESP32 netværk

God eksamensstruktur når du skal forklare en opgave:

1. Vis/topologi: hvilke enheder og subnets er med?
2. Forklar IP-plan: hvem har hvilken IP, gateway og subnetmask?
3. Forklar protokollen: ARP, DHCP, DNS, MQTT, SSH osv.
4. Vis konfiguration: router, PC, service eller program.
5. Test: `ping`, `traceroute`, `Wireshark`, `show route`, `dig`, `mosquitto_pub`.
6. Konklusion: hvad beviser testen?

Gode standard tests:

```sh
ip a
ip route
ping <gateway>
ping <anden-host>
traceroute <destination>
```

På Windows:

```powershell
ipconfig
ping <ip>
tracert <ip>
```

På Juniper SRX:

```text
show interfaces terse
show route
show route protocol static
show configuration routing-options
show security zones
show security policies
```

Wireshark-filtre:

```text
arp
icmp
dns
dhcp
tcp.port == 1883
ssh
http
```

