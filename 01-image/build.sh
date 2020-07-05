#!/bin/bash

set -e

export PATH="$(pwd)/bin:${PATH}"
export $(cat ../ENVIRONMENT)

./util/yaml2json.py < packer.yaml > packer.tmp.json

packer validate packer.tmp.json
packer build "$@" packer.tmp.json 

SNAPSHOT_ID=$(./util/getManifest.py < manifest.json)
cat > ./snapshot.tfvars <<EOF
snapshot_id="${SNAPSHOT_ID}"
EOF
