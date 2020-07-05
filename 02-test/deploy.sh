#!/bin/bash

set -e

export PATH="$(pwd)/../bin:${PATH}"
export $(cat ../ENVIRONMENT)

terraform init
terraform validate
terraform plan -var-file ../01-image/snapshot.tfvars -out=tfplan
terraform apply tfplan