# Switch, ARP og STP

## Switch vs hub

En hub sender alle frames ud på alle porte. Den forstår ikke MAC-adresser.

En switch lærer MAC-adresser og sender normalt kun frames ud på den port hvor modtageren findes.

Switchens MAC-tabel fungerer ca. sådan:

```text
MAC address -> port/interface
```

Hvis switchen ikke kender destinationens MAC, flooder den framen ud på flere porte.

## Linux bridge som switch

I opgaverne blev en Linux bridge brugt som virtuel switch.

Installer værktøjer:

```sh
sudo apt update
sudo apt install bridge-utils ifupdown
```

Se interfaces:

```sh
ip a
ip a | grep ens
```

Opret bridge:

```sh
sudo brctl addbr br0
```

Tilføj interfaces til bridge:

```sh
sudo brctl addif br0 ens33
sudo brctl addif br0 ens37
sudo brctl addif br0 ens38
```

Start bridge:

```sh
sudo ifup br0
```

Se bridges:

```sh
brctl show
```

Se MAC-tabel:

```sh
sudo brctl showmacs br0
```

## ARP

ARP oversætter IPv4-adresse til MAC-adresse på det lokale netværk.

Eksempel:

```text
Who has 192.168.1.20? Tell 192.168.1.10
192.168.1.20 is at aa:bb:cc:dd:ee:ff
```

Se ARP/neighbour table:

```sh
ip neigh show
arp -n
```

Tøm ARP table:

```sh
sudo ip neigh flush all
```

God demo:

```sh
sudo ip neigh flush all
ip neigh show
ping <anden-ip> -c 1
ip neigh show
```

I Wireshark:

```text
arp
icmp || arp
```

Eksamensforklaring:

Før en host kan sende en IP-pakke på lokalt netværk, skal den kende modtagerens MAC-adresse. Hvis den ikke kender den, sender den en ARP request som broadcast. Modtageren svarer med ARP reply, og derefter kan ICMP/ping sendes.

## STP

STP står for Spanning Tree Protocol.

Problem: Hvis switches forbindes med loop, kan broadcasts køre rundt igen og igen. Det kan skabe broadcast storm.

STP løser det ved at blokere en redundant port, så der stadig findes fysisk redundancy, men ikke et aktivt loop.

Slå STP fra på Linux bridge:

```sh
sudo brctl stp br0 off
```

Slå STP til:

```sh
sudo brctl stp br0 on
```

Wireshark tegn på broadcast storm:

```text
ff:ff:ff:ff:ff:ff
```

God eksamensforklaring:

STP forhindrer loops på lag 2. Uden STP kan broadcast frames blive sendt rundt i ring, fordi Ethernet frames ikke har TTL ligesom IP-pakker.

