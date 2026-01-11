#!/bin/bash
set -euo pipefail
source /home/mario/Escritorio/keyflow/parts/gnome/sdk/run/environment.sh
set -x
make -j"12"
make -j"12" install DESTDIR="/home/mario/Escritorio/keyflow/parts/gnome/sdk/install"
