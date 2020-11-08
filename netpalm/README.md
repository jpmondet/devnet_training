# Netpalm

## Quick usage

- Need last docker-compose version [from here](https://github.com/docker/compose/releases)
- Which depends on `python-pyparsing` (yeah python2's one..)
- Get [netpalm](https://github.com/tbotnz/netpalm)'s repo
- `docker-compose up -d --build` with the docker-compose.yml provided
  - Configs should be modified/reviewed (the most important file is `config.json` and is located in `config/`)
- `curl -H "accept: application/json" -H "X-Api-Key: $(cat config/config.json | jq -r .api_key)" $(docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' netpalm_netpalm-controller_1):9000/workers`

## Actually doing somethin'

By browsing to `http://$(docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' netpalm_netpalm-controller_1):9000`, we get access to the neat swagger docs.

See an example of getting config from a network device in `getconfig.py`
