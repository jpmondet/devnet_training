# Puppet for Netdevices


## Trying with [N9K container](https://github.com/jpmondet/dockerized_n9kv)

`docker run -d --name nxos --privileged myregistry/nxos:7.0.3`

`docker run --name puppet --hostname puppet -v ./puppet_code:/etc/puppetlabs/code puppet/puppetserver`

The module [ciscopuppet](https://forge.puppet.com/modules/puppetlabs/ciscopuppet) is necessary on the puppet master  
even for a agentless install.  
(Yeah I'm opting for agentless. The agent usage is an [horror movie](https://github.com/cisco/cisco-network-puppet-module/blob/master/docs/README-agent-install.md). Definitely not production-ready.)

`puppet module install puppetlabs-ciscopuppet`  
`mkdir /etc/puppetlabs/puppet/devices/`  
`echo "172.17.0.2 n9k.local.lab" >> /etc/hosts`  


**Testing the settup : `puppet device --verbose --target n9k.local.lab`**


