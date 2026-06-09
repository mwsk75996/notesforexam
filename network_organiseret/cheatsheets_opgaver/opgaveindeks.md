# Opgave- og Noteindeks for Netværk

Dette indeks linker til de emne-opdelte noter og tilhørende filer i den organiserede netværksmappe.

## Emner og Noter

*   **01. IP-Subnetting & Binær:**
    *   [ip-subnetting.md](file:///home/matt/Notes/notesforexam/network_organiseret/01_ip_subnetting/ip-subnetting.md) — IPv4, oktetter, binær omregning, CIDR, private IP-blokke og APIPA.
*   **02. Switch, ARP og STP:**
    *   [switch-arp-stp.md](file:///home/matt/Notes/notesforexam/network_organiseret/02_switch_arp_stp/switch-arp-stp.md) — Forskellen på Hub og Switch, opsætning af Linux bridge, ARP-processen, samt STP (Spanning Tree Protocol) og loops.
*   **03. Routing & vSRX (Firewall):**
    *   [routing-og-srx.md](file:///home/matt/Notes/notesforexam/network_organiseret/03_routing_vsrx/routing-og-srx.md) — Lag 3 routing-principper, statisk routing, og grundlæggende Juniper SRX opsætning.
    *   [vsrx-config-forklaringer.md](file:///home/matt/Notes/notesforexam/network_organiseret/03_routing_vsrx/vsrx-config-forklaringer.md) — Gennemgang af vSRX konfigurationer (Interface IP, default route, zones, policies og source NAT).
    *   [srx-security-zones.md](file:///home/matt/Notes/notesforexam/network_organiseret/03_routing_vsrx/srx-security-zones.md) — Logisk segmentering, security zones, inbound traffic tilladelser og security policies.
*   **04. DHCP, DNS og NAT:**
    *   [dhcp-dns-nat.md](file:///home/matt/Notes/notesforexam/network_organiseret/04_dhcp_dns_nat/dhcp-dns-nat.md) — DHCP DORA processen, DNS navneopløsning (med dnsmasq og dig/nslookup), samt Source NAT opsætning.
*   **05. Netværkstjenester & Web:**
    *   [nginx-webserver.md](file:///home/matt/Notes/notesforexam/network_organiseret/05_services_web/nginx-webserver.md) — Installation af Nginx, server blocks (virtuelle hosts), reverse proxy opsætning, og log-overvågning.
    *   [ssh.md](file:///home/matt/Notes/notesforexam/network_organiseret/05_services_web/ssh.md) — Fjernadgang med OpenSSH, administration af host keys (`known_hosts`), og sikker filkopiering med SCP.
*   **06. IoT og MQTT:**
    *   [mqtt.md](file:///home/matt/Notes/notesforexam/network_organiseret/06_iot_mqtt/mqtt.md) — Publish/Subscribe-model, Mosquitto broker opsætning, terminal-tests, QoS (Quality of Service) niveauer og Wireshark analyser.
    *   [esp32-og-iot.md](file:///home/matt/Notes/notesforexam/network_organiseret/06_iot_mqtt/esp32-og-iot.md) — ESP32 som WiFi Access Point/Webserver, ESP-NOW (direkte peer-to-peer kommunikation uden AP), og integration med MQTT.
*   **07. Fejlfinding & Wireshark:**
    *   [wireshark-og-fejlfinding.md](file:///home/matt/Notes/notesforexam/network_organiseret/07_fejlfinding_wireshark/wireshark-og-fejlfinding.md) — Fejlsøgningsstrategi med `ping` og `traceroute`, TCP three-way handshake (SYN, SYN/ACK, ACK), samt Wireshark display-filtre.
*   **08. Eksamenscheatsheets & Overblik:**
    *   [overblik.md](file:///home/matt/Notes/notesforexam/network_organiseret/cheatsheets_opgaver/overblik.md) — Overordnet emneliste, test-flow og Wireshark filteroverblik.
    *   [kommando-cheatsheet.md](file:///home/matt/Notes/notesforexam/network_organiseret/cheatsheets_opgaver/kommando-cheatsheet.md) — Kvik-reference for Linux netværkskommandoer, Windows netværk, vSRX konfiguration, Nginx, SSH, MQTT og Wireshark.
    *   [eksamens-netvaerk-forberedelse.md](file:///home/matt/Notes/notesforexam/network_organiseret/cheatsheets_opgaver/eksamens-netvaerk-forberedelse.md) — Detaljeret cheatsheet til forberedelse af det specifikke eksamensnetværk (vSRX R1, PC3 og PC4 maskinerne) baseret på eksamensforberedelsesdokumentet.

---

## Opgaveindeks

Oversigt over de afleveringsopgaver (Assignments) vi har lavet igennem 1 & 2 semester:

```text
Assignment 4      Switch, hub, Linux bridge, MAC table
Assignment 5      STP, switch loop, broadcast storm
Assignment 6      Binær, IP, subnetting, netværksdesign
Assignment 10     Routing, en router, to subnets
Assignment 11     Routing, to routere, fem subnets, vSRX
Assignment 14     ARP table, ARP process, broadcast
Assignment 15     Fysisk netværk med switch
Assignment 16     Linux routing table, default gateway
Assignment 18     DHCP, DORA, APIPA, DHCP relay
Assignment 20     ESP32 access point, webserver, TCP handshake, HTTP
Assignment 21     ESP-NOW mellem ESP32-enheder
Assignment 27     Routing på fysisk SRX240
Assignment 28     To fysiske routere, fem subnets
Assignment 32     Source NAT på fysisk SRX
Assignment 42     DNS server, dnsmasq, dig, nslookup
Assignment 53/54  SRX security zones og policies
Assignment 57     MQTT med C++ og Mosquitto
Assignment 58     SSH basics med OpenSSH host/server keys
Assignment 59     SSH med klientnøgler og scp
Assignment 62     MQTT på ESP32 med C++
Assignment 63     MQTT analyse i Wireshark, QoS, HiveMQ
```

---

## Ressourcer og filer

*   **Netværksdiagrammer:** [diagrammer/](file:///home/matt/Notes/notesforexam/network_organiseret/diagrammer/) (SVGs med topologier for de forskellige Assignments)
*   **vSRX Konfigurationsfiler:** [vsrx_configs/](file:///home/matt/Notes/notesforexam/network_organiseret/vsrx_configs/) (Eksempler på rå JSON-konfigurationer fra opgaverne)
