# IP, binær og subnetting

IPv4-adresser består af 32 bits delt i 4 oktetter.

Eksempel:

```text
192.168.1.10
```

Hver del er 8 bits:

```text
192 = 11000000
168 = 10101000
1   = 00000001
10  = 00001010
```

CIDR fortæller hvor mange bits der er netværksdelen:

```text
192.168.1.10/24
```

`/24` betyder:

```text
Subnetmask: 255.255.255.0
Netværk:    192.168.1.0
Broadcast:  192.168.1.255
Hosts:      192.168.1.1 - 192.168.1.254
```

Hurtig host-formel:

```text
brugbare hosts = 2^(host bits) - 2
```

Eksempel `/26`:

```text
32 - 26 = 6 host bits
2^6 - 2 = 62 brugbare hosts
```

Nyttige subnetmasker:

```text
/24 = 255.255.255.0     = 254 hosts
/25 = 255.255.255.128   = 126 hosts
/26 = 255.255.255.192   = 62 hosts
/27 = 255.255.255.224   = 30 hosts
/28 = 255.255.255.240   = 14 hosts
/30 = 255.255.255.252   = 2 hosts
```

`/30` er god til router-til-router links, fordi der kun skal bruges 2 IP'er.

Private IP ranges:

```text
10.0.0.0/8
172.16.0.0/12
192.168.0.0/16
```

APIPA:

```text
169.254.0.0/16
```

APIPA bruges hvis en klient ikke får DHCP-adresse. Den vælger selv en adresse i `169.254.x.x`.

Linux commands:

```sh
ip a
ip route
ping 192.168.1.1 -c 3
```

Windows commands:

```powershell
ipconfig
ping 192.168.1.1
```

God eksamensforklaring:

En IP-adresse identificerer en host på lag 3. Subnetmasken fortæller hvilken del af IP-adressen der er netværket, og hvilken del der er hosten. Hvis destinationen ligger uden for eget subnet, sendes pakken til default gateway.

