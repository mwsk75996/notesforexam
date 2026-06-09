# MariaDB C++ example

Dette eksempel viser et lille C++ program der bruger MariaDB/MySQL C client library.

Projektet bruger:

- CMake
- `pkg-config`
- MariaDB client library (`libmariadb`)
- `g++`

## Installer dependencies

Arch/CachyOS:

```sh
sudo pacman -S cmake pkgconf mariadb-libs
```

Debian/Ubuntu:

```sh
sudo apt install cmake pkg-config g++ libmariadb-dev
```

Fedora:

```sh
sudo dnf install cmake pkgconf-pkg-config gcc-c++ mariadb-connector-c-devel
```

## Tjek at library findes

CMake bruger denne linje:

```cmake
pkg_check_modules(MARIADB REQUIRED libmariadb)
```

Derfor skal denne kommando virke:

```sh
pkg-config --libs --cflags libmariadb
```

Hvis den fejler med `Package 'libmariadb' not found`, mangler MariaDB client development/library pakken.

## Build og kør

Kør smoke test:

```sh
./run_catch.sh
```

Kør programmet:

```sh
./run_main.sh
```

Programmet spørger efter MariaDB username og password, og prøver at forbinde til en MariaDB server på `localhost`.

## Vigtigt

`mariadb-libs` / `libmariadb-dev` er kun client library. Det er nok til at compile programmet, men for at `run_main.sh` kan forbinde, skal der også køre en MariaDB server på maskinen eller på den host programmet forbinder til.
