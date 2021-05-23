provider "docker" {
  host = "tcp://127.0.0.1:2376/"
}

resource "docker_container" "foo" {
  name  = "foo"
  image = docker_image.ubuntu.latest
  attach = false
  must_run = true
  command = ["sleep", "infinity"]
}

resource "docker_image" "ubuntu" {
  name = "ubuntu:latest"
}
