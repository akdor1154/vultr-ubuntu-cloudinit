provider "vultr" {

}

variable "snapshot_id" {
    type = string
    validation {
        condition = length(var.snapshot_id) > 0
        error_message = "The snapshot_id was empty!"
    }
}

variable "ssh_key_ids" {
    type = list(string)
}

resource "vultr_server" "server" {
    region_id = "19" # Sydney https://api.vultr.com/v1/regions/list
    plan_id = "202" # 2GB Ram, 55GB SSD, 1 cpu https://api.vultr.com/v1/plans/list?type=vc2
    snapshot_id = var.snapshot_id
    hostname = "vultr-server"
    label = "Ubuntu 20.04 Server"
    ssh_key_ids = var.ssh_key_ids
    enable_ipv6 = true
    user_data = <<EOCC
#cloud-config

EOCC
}

output "server_ip" {
    value="${vultr_server.server.main_ip}"
}

terraform {
  experiments = [variable_validation]
}
