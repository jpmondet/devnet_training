class ciscopuppet::proxy (String $repo = 'https://rubygems.org', String $proxy = '') {

  include resource_api::agent

  # Process proxy settings 
  if $proxy == '' {
    $opts = {}
  }
  else {
    $opts = { '--http-proxy' => $proxy }
  }

  package { 'cisco_node_utils' :
    ensure          => present,
    provider        => 'puppet_gem',
    source          => $repo,
    install_options => $opts,
  }

  package { 'net_http_unix' :
    ensure          => present,
    provider        => 'puppet_gem',
    source          => $repo,
    install_options => $opts,
  }
}
