# MQTT og SSH

## MQTT

MQTT er en letvægts applikationslagsprotokol, ofte brugt til IoT.

Roller:

- Broker: central server
- Publisher: sender beskeder
- Subscriber: modtager beskeder
- Topic: kanalnavn
- Payload: beskedindhold

Standard port:

```text
1883 TCP
```

MQTT over TLS:

```text
8883 TCP
```

Installer Mosquitto på Linux:

```sh
sudo apt update
sudo apt install mosquitto mosquitto-clients
```

Start broker:

```sh
sudo systemctl start mosquitto
sudo systemctl enable mosquitto
sudo systemctl status mosquitto
```

3-konsol demo:

Konsol 1:

```sh
mosquitto -v
```

Konsol 2:

```sh
mosquitto_sub -h localhost -t test -v
```

Konsol 3:

```sh
mosquitto_pub -h localhost -t test -m "hello mqtt"
```

Publish med QoS:

```sh
mosquitto_pub -h 172.20.10.12 -p 1883 -i Test -t esp32/temp -m "23.4" -q 1
```

QoS:

- 0: fire and forget
- 1: at least once, kræver PUBACK
- 2: exactly once, bruger PUBLISH, PUBREC, PUBREL, PUBCOMP

Wireshark:

```text
tcp.port == 1883
mqtt
```

God eksamensforklaring:

MQTT bruger broker-modellen, så publisher og subscriber ikke behøver kende hinanden direkte. De skal bare bruge samme broker og topic.

## SSH

SSH bruges til krypteret remote login.

Installer OpenSSH:

```sh
sudo apt update
sudo apt install openssh-client openssh-server -y
```

Start SSH server:

```sh
sudo systemctl enable ssh
sudo systemctl start ssh
sudo systemctl status ssh
```

Tillad SSH i firewall:

```sh
sudo ufw allow ssh
```

Login:

```sh
ssh bruger@192.168.10.10
```

Eksempel:

```sh
ssh karen@192.168.10.10
```

Opret bruger:

```sh
sudo adduser karen
```

Host keys ligger typisk her:

```text
/etc/ssh/ssh_host_ed25519_key
/etc/ssh/ssh_host_ed25519_key.pub
```

Kendte servere gemmes her:

```text
~/.ssh/known_hosts
```

Secure copy:

```sh
scp file.txt bruger@192.168.10.10:/home/bruger/
```

Wireshark filter:

```text
ssh
tcp.port == 22
```

God eksamensforklaring:

Første gang man forbinder til en SSH-server, accepterer man serverens host key. Den gemmes i `known_hosts`, så klienten senere kan opdage hvis serverens identitet ændrer sig.

