# Testing SONiC

# Quick usage with gns3


`wget --continue https://sonic-jenkins.westus2.cloudapp.azure.com/job/vs/job/buildimage-vs-image-202012/lastSuccessfulBuild/artifact/target/sonic-vs.img.gz`

`wget https://raw.githubusercontent.com/Azure/sonic-buildimage/master/platform/vs/sonic-gns3a.sh`

`gzip -d sonic-vs.img.gz`

`chmod u+x sonic-gns3a.sh`

`./sonic-gns3a.sh -b sonic-vs.img`

Then import appliance `SONiC-latest.gns3a` into gns3
