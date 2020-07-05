# Cloud-Init enabled Ubuntu for Vultr

This repo will build a snapshot for you which you can use as a base image for Ubuntu 20.04 on Vultr.

New servers created with this snapshot:
 - disable root login by ssh
 - set up the default `ubuntu` user, and provision it with the SSH keys you've configured to launch it with in the Vultr console / API. Password login is disabled, so **if you don\'t provide SSH keys you won't be able to log in**.
 - process userdata with cloud-init properly.

You will need to set up `ENVIRONMENT` to create images, and additionally `02-test/terraform.tfvars` if you want to use the built-in terraform setup to test them.

Example userdata:
```yaml
#cloud-config
package_upgrade: true
packages:
  - python3
users:
  - default
  - name: my-app
```

## Usage

You will need to set up `ENVIRONMENT` to create images, and additionally `02-test/terraform.tfvars` if you want to use the built-in terraform setup to test them.

To pull deps: (linux only - the rest will be cross-platform if you have `terraform`, `packer-builder-vultr`, and `packer` in your path)
```sh
cd bin
./get-bins.sh
```

To build the image:
```sh
cd 01-image
./build.sh
```

To deploy a server based on the image:
```sh
cd 02-test
./deploy.sh
```

To undeploy the above server:
```sh
cd 02-test
./destroy.sh
```
