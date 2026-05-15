# Kommando cheatsheet

## Linux netværk

```sh
ip a
ip route
ip neigh show
arp -n
sudo ip neigh flush all
ping 8.8.8.8 -c 3
traceroute dr.dk
```

## Windows netværk

```powershell
ipconfig
ping 8.8.8.8
tracert dr.dk
```

## Linux bridge/switch

```sh
sudo apt install bridge-utils ifupdown
sudo brctl addbr br0
sudo brctl addif br0 ens33
sudo brctl addif br0 ens37
sudo ifup br0
brctl show
sudo brctl showmacs br0
sudo brctl stp br0 on
sudo brctl stp br0 off
```

## Juniper SRX

```text
configure
commit check
commit
show interfaces terse
show route
show route protocol static
show configuration
show configuration routing-options
show security zones
show security policies
```

Interface:

```text
set interfaces ge-0/0/1 unit 0 family inet address 192.168.10.1/24
```

Static route:

```text
set routing-options static route 192.168.20.0/24 next-hop 10.10.10.2
```

## DHCP/DNS

```sh
dig awesome.dk
dig @192.168.10.10 awesome.dk
nslookup awesome.dk
nslookup awesome.dk 192.168.10.10
```

## MQTT

```sh
sudo apt install mosquitto mosquitto-clients
sudo systemctl start mosquitto
sudo systemctl status mosquitto
mosquitto -v
mosquitto_sub -h localhost -t test -v
mosquitto_pub -h localhost -t test -m "hello mqtt"
mosquitto_pub -h localhost -t test -m "qos test" -q 1
```

## SSH

```sh
sudo apt install openssh-client openssh-server -y
sudo systemctl enable ssh
sudo systemctl start ssh
sudo systemctl status ssh
ssh user@192.168.10.10
scp file.txt user@192.168.10.10:/home/user/
sudo adduser karen
```

## Wireshark filters

```text
arp
icmp
icmp || arp
dns
dhcp
bootp
http
ssh
tcp.port == 22
tcp.port == 1883
udp.port == 53
udp.port == 67 || udp.port == 68
eth.dst == ff:ff:ff:ff:ff:ff
```

