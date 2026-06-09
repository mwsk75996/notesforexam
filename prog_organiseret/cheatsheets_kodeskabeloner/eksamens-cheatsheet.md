# Eksamens-cheatsheet: MariaDB, MQTT og Bash-integration

Dette cheatsheet dækker de specifikke programmeringskrav og testforberedelser, der er beskrevet i eksamensforberedelsens PDF.

---

## 1. MariaDB Database & Tabelopsætning

Her er SQL-kommandoerne til at oprette databasen `Sensordata` og tabellen med de tre krævede kolonner:
- `Temperaturmåling` (Double)
- `Tidsstempel` (Timestamp, indsættes automatisk ved oprettelse)
- `Device ID` (Varchar, med backticks ` ` for at tillade mellemrum i kolonnenavnet)

```sql
-- Opret databasen
CREATE DATABASE IF NOT EXISTS Sensordata;
USE Sensordata;

-- Opret tabellen med de 3 specifikke kolonner
CREATE TABLE IF NOT EXISTS temperatur_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    `Temperaturmåling` DOUBLE NOT NULL,
    `Tidsstempel` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `Device ID` VARCHAR(50) NOT NULL
);

-- Test indsættelse manuelt
INSERT INTO temperatur_log (`Temperaturmåling`, `Device ID`) VALUES (23.85, 'ESP32_TEST_DEVICE');

-- Se data
SELECT * FROM temperatur_log;
```

---

## 2. Shell Script: MQTT til MariaDB (mosquitto_sub & mysql cli)

Dette shell-script skal køre i baggrunden på PC3. Det lytter (subscribes) på et MQTT-emne, modtager en JSON-payload, udpakker værdierne med `jq` og indsætter dem direkte i din MariaDB-database.

### Forudsætninger:
Installer `jq` (JSON parser) og `mosquitto-clients` på Linux:
```bash
sudo apt update && sudo apt install jq mosquitto-clients
```

### Script (`mqtt_to_mariadb.sh`):
```bash
#!/bin/bash

# Database konfiguration
DB_USER="root"
DB_PASS="dit_mariadb_kodeord"
DB_NAME="Sensordata"
DB_TABLE="temperatur_log"

# MQTT konfiguration
MQTT_BROKER="localhost" # PC3 kører typisk brokeren selv
MQTT_TOPIC="esp32/sensor_data"

echo "Lytter på MQTT topic: $MQTT_TOPIC og indsætter i MariaDB..."

# Kør mosquitto_sub og loop over indkommende payloads
mosquitto_sub -h "$MQTT_BROKER" -t "$MQTT_TOPIC" | while read -r line
do
    echo "Modtog besked: $line"
    
    # Udpak værdier fra JSON payload (fx: {"temp": 24.5, "device_id": "ESP32_1"})
    temp=$(echo "$line" | jq -r '.temp')
    device_id=$(echo "$line" | jq -r '.device_id')
    
    # Valider at vi har fået korrekte data
    if [ -n "$temp" ] && [ -n "$device_id" ]; then
        echo "Indsætter: Temp=$temp, Device=$device_id"
        
        # SQL Insert (Tidsstempel sættes automatisk af MariaDB)
        mysql -u "$DB_USER" -p"$DB_PASS" -e \
        "INSERT INTO ${DB_NAME}.${DB_TABLE} (\`Temperaturmåling\`, \`Device ID\`) VALUES ($temp, '$device_id');"
        
        if [ $? -eq 0 ]; then
            echo "Indsæt succesfuld!"
        else
            echo "Fejl under database-indsæt!"
        fi
    else
        echo "Ugyldig eller ufuldstændig JSON modtaget."
    fi
    echo "--------------------------------------"
done
```

---

## 3. C++ MariaDB Client (Test Indsættelse)

C++ program der forbinder til din lokale database og indsætter en testmåling.

### Kildekode (`mariadb_client.cpp`):
```cpp
#include <iostream>
#include <mysql/mysql.h>

int main() {
    MYSQL* conn;
    conn = mysql_init(NULL);

    if (conn == NULL) {
        std::cerr << "Fejl ved initialisering af MySQL objekt!" << std::endl;
        return 1;
    }

    // Forbind til serveren (host, user, password, database, port, socket, client_flag)
    if (mysql_real_connect(conn, "localhost", "root", "dit_mariadb_kodeord", "Sensordata", 3306, NULL, 0) == NULL) {
        std::cerr << "Forbindelsesfejl: " << mysql_error(conn) << std::endl;
        mysql_close(conn);
        return 1;
    }

    std::cout << "Forbundet til MariaDB database!" << std::endl;

    // Definer SQL-måling (Tidsstempel oprettes automatisk)
    double temp = 25.4;
    std::string device_id = "CPP_TEST_CLIENT";
    
    char query[256];
    sprintf(query, "INSERT INTO temperatur_log (`Temperaturmåling`, `Device ID`) VALUES (%.2f, '%s')", temp, device_id.c_str());

    // Kør forespørgsel
    if (mysql_query(conn, query)) {
        std::cerr << "Indsættelsesfejl: " << mysql_error(conn) << std::endl;
    } else {
        std::cout << "Data succesfuldt indsat i tabellen!" << std::endl;
    }

    // Luk forbindelse
    mysql_close(conn);
    return 0;
}
```

---

## 4. C++ MQTT Publisher Client

Et C++ program der forbinder til MQTT brokeren på PC3 og sender en testbesked.

### Kildekode (`mqtt_publisher.cpp`):
```cpp
#include <iostream>
#include <cstring>
#include <mqtt/async_client.h> // Kræver Paho MQTT C++ library

const std::string ADDRESS("tcp://localhost:1883");
const std::string CLIENT_ID("CPP_Publisher");
const std::string TOPIC("esp32/sensor_data");

int main() {
    // Opret klient
    mqtt::async_client client(ADDRESS, CLIENT_ID);

    mqtt::connect_options connOpts;
    connOpts.set_keep_alive_interval(20);
    connOpts.set_clean_session(true);

    try {
        std::cout << "Forbinder til MQTT broker..." << std::endl;
        client.connect(connOpts)->wait();
        std::cout << "Forbundet!" << std::endl;

        // Opret JSON Payload
        std::string payload = "{\"temp\": 22.8, \"device_id\": \"CPP_CLIENT_1\"}";

        // Send besked (Publish)
        std::cout << "Sender besked: " << payload << std::endl;
        mqtt::message_ptr pubmsg = mqtt::make_message(TOPIC, payload);
        pubmsg->set_qos(1);
        client.publish(pubmsg)->wait();
        std::cout << "Besked sendt!" << std::endl;

        // Afbryd forbindelse
        client.disconnect()->wait();
        std::cout << "Afbrudt." << std::endl;
    }
    catch (const mqtt::exception& exc) {
        std::cerr << "MQTT Fejl: " << exc.what() << std::endl;
        return 1;
    }

    return 0;
}
```

---

## 5. CMakeLists.txt til kompilering (PC)

Når du skal kompilere dine C++ test-klienter, skal du bruge dette `CMakeLists.txt` for at linke korrekt til MariaDB og Paho MQTT bibliotekerne:

```cmake
cmake_minimum_required(VERSION 3.10)
project(EksamensTestClient)

set(CMAKE_CXX_STANDARD 11)

# Find MariaDB/MySQL klientbiblioteker
# På Ubuntu installeres de med: sudo apt install libmariadb-dev eller libmysqlclient-dev
find_path(MYSQL_INCLUDE_DIR mysql/mysql.h)
find_library(MYSQL_LIBRARY mysqlclient)

# Find Paho MQTT C++ bibliotek
# Installeres med: sudo apt install libpaho-mqtt-dev libpaho-mqttpp-dev
find_package(PahoMqttCpp REQUIRED)

# 1. Byg MariaDB C++ Client
add_executable(mariadb_test mariadb_client.cpp)
target_include_directories(mariadb_test PRIVATE ${MYSQL_INCLUDE_DIR})
target_link_libraries(mariadb_test ${MYSQL_LIBRARY})

# 2. Byg MQTT C++ Client
add_executable(mqtt_test mqtt_publisher.cpp)
target_link_libraries(mqtt_test paho-mqttpp3 paho-mqtt3a)
```
