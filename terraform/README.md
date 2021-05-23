# Terraform usage


Looking at the providers, it seems like the easiest way to try locally is by using `docker provider`

(Had to enable docker api though 
 `vi /lib/systemd/system/docker.service`  
 `ExecStart=/usr/bin/dockerd -H=fd:// -H=tcp://127.0.0.1:2376`  
 `sudo systemctl daemon-reload`  
 `sudo systemctl restart docker`)


For example, with a `main.tf` file containing : 

```
terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
    }
  }
}

# Configure the Docker provider
provider "docker" {
  host = "tcp://127.0.0.1:2376/"
}

# Create a container
resource "docker_container" "foo" {
  image = docker_image.ubuntu.latest
  name  = "foo"
}

resource "docker_image" "ubuntu" {
  name = "ubuntu:latest"
}
```

We can create a container after this steps : 

`terraform init`  (this will download the docker provider and prepare the current directory)

`terraform plan -out testPlan` (optional but validates the config & shows the steps that will be applied by terraform. By specify in `-out` file, terraform will  
encode the steps into a file to ensure that at `apply` time, those exact steps will be applied)

`terraform apply testPlan`


**WARNING:** With the above config, even if Terraform says that everything will be ok, it won't !

It gives a "very" explicit error (sic): 

```
Error: Container a26c30c0ca030c0a9681b26d3d45710a1709c3f06ea1a4d77c13c31049c5cd73 exited after creation, error was:

  with docker_container.foo,
  on docker.tf line 5, in resource "docker_container" "foo":
   5: resource "docker_container" "foo" {
```

Had to pull my hair on this...  
It seems that Terraform can't retrieve the state of the container because the ubuntu image defaults to `/bin/bash`

To override that, we can add to the "foo" resource : 

```
  attach = false
  must_run = true
  command = ["sleep", "infinity"]
```

Then it works ok.


Finally, we can destroy the infrastructure : `terraform destroy`
