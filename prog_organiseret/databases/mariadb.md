# Databaser og MariaDB

Repo-eksempel i denne mappe:

- `mariadb_example/`

MariaDB er en relationel database. Man gemmer data i tabeller med rækker og kolonner, og man bruger SQL til at læse og ændre data.

## Vigtige ord

- Database: samling af tabeller
- Table: struktur med kolonner og rækker
- Row: én post i tabellen
- Column: ét felt, fx `id`, `name`, `temperature`
- Primary key: unik ID for en række
- SQL: sprog til queries
- Client library: C/C++ library der forbinder programmet til databasen

## Typiske SQL commands

```sql
CREATE DATABASE sensor_db;
USE sensor_db;

CREATE TABLE readings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sensor_name VARCHAR(50),
    temperature DOUBLE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO readings (sensor_name, temperature)
VALUES ('DS18B20', 23.4);

SELECT * FROM readings;
```

## C++ og MariaDB client library

Include:

```cpp
#include <mariadb/mysql.h>
```

Minimal connection:

```cpp
MYSQL* conn = mysql_init(nullptr);

if (!mysql_real_connect(conn, "localhost", username, password, nullptr, 0, nullptr, 0)) {
    std::cout << "Connection failed: " << mysql_error(conn) << "\n";
    mysql_close(conn);
    return 1;
}

std::cout << "Connected to MariaDB\n";
mysql_close(conn);
```

## CMake

`mariadb_example` bruger `pkg-config` til at finde `libmariadb`:

```cmake
find_package(PkgConfig REQUIRED)
pkg_check_modules(MARIADB REQUIRED libmariadb)

target_include_directories(main PRIVATE ${MARIADB_INCLUDE_DIRS})
target_link_directories(main PRIVATE ${MARIADB_LIBRARY_DIRS})
target_link_libraries(main PRIVATE ${MARIADB_LIBRARIES})
```

## Installation

Arch/CachyOS:

```sh
sudo pacman -S cmake pkgconf mariadb-libs
```

Debian/Ubuntu:

```sh
sudo apt install cmake pkg-config g++ libmariadb-dev
```

Tjek:

```sh
pkg-config --libs --cflags libmariadb
```

## Vigtigt

MariaDB client library er nok til at compile C++ programmet. For at programmet faktisk kan forbinde, skal der også køre en MariaDB server på den host man forbinder til.

God eksamensforklaring:

Programmet er en database client. Det bruger MariaDB client library til at åbne en TCP/socket-forbindelse til serveren, logge ind med username/password og sende SQL queries.
