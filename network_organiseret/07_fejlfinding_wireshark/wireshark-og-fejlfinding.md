# Wireshark og fejlfinding

Wireshark bruges til at bevise hvad der faktisk sker på netværket.

Gode display filters:

```text
arp
icmp
icmp || arp
dns
dhcp
http
ssh
tcp
tcp.port == 1883
udp.port == 67 || udp.port == 68
udp.port == 53
```

Capture filter til MQTT:

```text
tcp port 1883
```

## Ping

Ping tester om en host svarer på ICMP.

```sh
ping 192.168.1.1 -c 3
ping 8.8.8.8 -c 3
ping dr.dk -c 3
```

Fejlsøgning med ping:

1. Ping egen gateway
2. Ping anden host i samme subnet
3. Ping host i andet subnet
4. Ping ekstern IP, fx `8.8.8.8`
5. Ping domæne, fx `dr.dk`

Hvis IP virker men domæne ikke virker: DNS-problem.

## Traceroute

Traceroute viser hvilke router-hop pakken tager.

```sh
traceroute 192.168.13.13
traceroute dr.dk
```

Windows:

```powershell
tracert dr.dk
```

God forklaring:

Traceroute er nyttig hvis ping fejler, fordi man kan se hvor langt pakken kommer før den stopper.

## ARP i Wireshark

Før ping på lokalt netværk ser man ofte:

```text
ARP request
ARP reply
ICMP echo request
ICMP echo reply
```

## TCP three-way handshake

TCP starter med:

```text
SYN -> SYN/ACK -> ACK
```

Bruges før fx HTTP, SSH og MQTT over TCP.

Hvis man prøver en forkert port, kan man se:

```text
SYN -> RST, ACK
```

Det betyder ofte at der ikke lytter en service på den port.

## MAC vs IP i routing

I Wireshark ved routing:

- IP-adresser er ende-til-ende.
- MAC-adresser ændres for hvert subnet/hop.

God eksamenssætning:

MAC-adresser bruges lokalt på lag 2, mens IP-adresser bruges til routing på lag 3.

