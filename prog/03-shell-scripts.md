# Shell scripts til build og run

Et shell script kan samle `cmake -> build -> run` i én kommando.

Gør script executable:

```sh
chmod +x run.sh
```

Kør script:

```sh
./run.sh
```

Simpelt script:

```sh
#!/usr/bin/env sh
set -e

cmake -S . -B build
cmake --build build
./build/app
```

`set -e` betyder at scriptet stopper hvis en command fejler.

Bedre script der virker uanset hvor man kører det fra:

```sh
#!/usr/bin/env sh
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

cmake -S "$SCRIPT_DIR" -B "$SCRIPT_DIR/build"
cmake --build "$SCRIPT_DIR/build"
"$SCRIPT_DIR/build/app"
```

Script til et bestemt CMake target:

```sh
#!/usr/bin/env sh
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

cmake -S "$SCRIPT_DIR" -B "$SCRIPT_DIR/build"
cmake --build "$SCRIPT_DIR/build" --target publisher
"$SCRIPT_DIR/build/publisher"
```

Script der tjekker om en fil er tom:

```sh
if [ ! -s "$SCRIPT_DIR/src/subscriber.cpp" ]; then
  echo "subscriber.cpp is empty"
  exit 1
fi
```

Nyttige shell ting:

```sh
pwd                 # viser nuværende mappe
ls                  # viser filer
ls -la              # viser også skjulte filer
cd mappe            # gå ind i mappe
cd ..               # gå en mappe op
rm -rf build        # slet build mappe
```

