# MQTT

MQTT bruges til beskeder mellem programmer via en broker.

De vigtige roller:

- Broker: serveren der modtager og sender beskeder videre
- Publisher: sender beskeder til et topic
- Subscriber: lytter på et topic
- Topic: navnet på kanalen, fx `test` eller `sensor/room1`
- Payload: selve beskeden
- QoS: hvor sikkert beskeden skal leveres

Typisk lokal broker:

```text
mqtt://localhost:1883
```

## MQTT i terminalen

Til eksamen kan man nemt vise MQTT med 3 terminaler/konsoller:

1. Broker
2. Subscriber
3. Publisher

Konsol 1 - start broker:

```sh
mosquitto -v
```

`-v` betyder verbose, så man kan se forbindelser og beskeder i brokerens output.

Konsol 2 - lyt på et topic:

```sh
mosquitto_sub -h localhost -t test
```

Konsol 3 - publish en besked:

```sh
mosquitto_pub -h localhost -t test -m "hello mqtt"
```

Hvis alt virker, kommer `"hello mqtt"` frem i subscriber-konsollen.

Man kan også subscribe med mere info:

```sh
mosquitto_sub -h localhost -t test -v
```

Så viser den både topic og besked:

```text
test hello mqtt
```

Publish med QoS:

```sh
mosquitto_pub -h localhost -t test -m "qos message" -q 1
```

Subscribe med QoS:

```sh
mosquitto_sub -h localhost -t test -q 1
```

Subscribe til alle subtopics under `sensor/`:

```sh
mosquitto_sub -h localhost -t "sensor/#" -v
```

Publish til et sensor topic:

```sh
mosquitto_pub -h localhost -t "sensor/room1/temp" -m "23.4"
```

Gode terminal flags:

- `-h localhost`: broker host
- `-p 1883`: broker port
- `-t test`: topic
- `-m "hello"`: message/payload
- `-q 1`: QoS level
- `-v`: verbose output

Topic eksempel:

```text
test
sensor/room1
```

QoS:

- `0`: send én gang, ingen garanti
- `1`: leveres mindst én gang
- `2`: leveres præcis én gang, men er langsommere

Paho MQTT C++ include:

```cpp
#include "mqtt/async_client.h"
```

Publisher ide:

```cpp
const std::string SERVER_URI = "mqtt://localhost:1883";
const std::string TOPIC = "test";
const int QOS = 1;

mqtt::async_client client(SERVER_URI, "");
client.connect()->wait();

mqtt::topic topic(client, TOPIC, QOS);
topic.publish("hello from publisher")->wait();

client.disconnect()->wait();
```

Subscriber ide:

```cpp
const std::string SERVER_URI = "mqtt://localhost:1883";
const std::string CLIENT_ID = "subscriber_1";
const std::string TOPIC = "test";
const int QOS = 1;

mqtt::async_client client(SERVER_URI, CLIENT_ID);
client.connect()->wait();
client.subscribe(TOPIC, QOS)->wait();
```

I CMake skal Paho libraries linkes:

```cmake
target_link_libraries(publisher paho-mqttpp3 paho-mqtt3as)
target_link_libraries(subscriber paho-mqttpp3 paho-mqtt3as)
```

Debug checklist:

- Kører broker?
- Bruger publisher og subscriber samme topic?
- Bruger de samme broker URI?
- Har subscriber en unik `CLIENT_ID`?
- Er libraries linket i CMake?
- Hvis subscriber ikke modtager noget, så start subscriber før publisher.
