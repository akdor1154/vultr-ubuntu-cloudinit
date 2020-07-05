#!/bin/sh
set -e

curl -fL https://releases.hashicorp.com/packer/1.6.0/packer_1.6.0_linux_amd64.zip -o packer.zip
unzip -o packer.zip
rm packer.zip

curl -fL https://github.com/vultr/packer-builder-vultr/releases/download/v1.0.9/packer-builder-vultr_1.0.9_linux_64-bit.tar.gz -o packer-vultr.tar.gz
tar -xvf packer-vultr.tar.gz
rm packer-vultr.tar.gz

curl -fL https://releases.hashicorp.com/terraform/0.12.28/terraform_0.12.28_linux_amd64.zip -o terraform.zip
unzip -o terraform.zip
rm terraform.zip
