from p4utils.utils.topology import Topology
from p4utils.utils.sswitch_API import SimpleSwitchAPI

class RoutingController(object):

    def __init__(self):

        self.topo = Topology(db="topology.db")
        self.controllers = {}
        self.init()

    def init(self):
        self.connect_to_switches()
        self.reset_states()
        self.set_table_defaults()

    def reset_states(self):
        [controller.reset_state() for controller in self.controllers.values()]

    def connect_to_switches(self):
        for p4switch in self.topo.get_p4switches():
            thrift_port = self.topo.get_thrift_port(p4switch)
            self.controllers[p4switch] = SimpleSwitchAPI(thrift_port)

    def set_table_defaults(self):
        for controller in self.controllers.values():
            controller.table_set_default("ipv4_lpm", "drop", [])
            controller.table_set_default("ecmp_group_to_nhop", "drop", [])


    def get_conn_host_infos(self, p4switch):
        connected_hosts = self.topo.get_hosts_connected_to(p4switch)
        if connected_hosts:
            host = connected_hosts[0]
            switch_infos = self.topo.node(p4switch)
            host_mac = self.topo.get_host_mac(host)
            host_ip = self.topo.get_host_ip(host) + '/32'
            output_iface = self.topo.interface_to_port(p4switch,switch_infos[host]['intf'])
            return host_ip, host_mac, output_iface
        else:
            return None, None, None

    def add_ecmp_group(self, p4switch, ss_api, neigh, paths, ecmp_group):
        host_ip, host_mac, output_iface = self.get_conn_host_infos(neigh)
        if host_ip:
            next_hops = [path[1] for path in paths]
            dst_macs_ports = [(self.topo.node_to_node_mac(next_hop, p4switch),
                              self.topo.node_to_node_port_num(p4switch, next_hop))
                              for next_hop in next_hops]
            if ecmp_group.get(p4switch):
                if ecmp_group[p4switch].get(tuple(dst_macs_ports)):
                    ecmp_group[p4switch][tuple(dst_macs_ports)] = ecmp_group[p4switch][tuple(dst_macs_ports)] + 1
                else:
                    ecmp_group[p4switch][tuple(dst_macs_ports)] = 1
            else:
                ecmp_group[p4switch] = {}
                ecmp_group[p4switch][tuple(dst_macs_ports)] = 1

            print('Adding multipath entries')
            ss_api.table_add('ipv4_lpm', 'ecmp_group', [host_ip] ,[str(1), str(len(next_hops))])
            index = 0
            for dst_mac_port in dst_macs_ports:
                ss_api.table_add('ecmp_group_to_nhop', 'set_nhop', [str(1),str(index)] ,[dst_mac_port[0], str(dst_mac_port[1])])
                index = index + 1
            
        return None

    def add_route_via_best(self, p4switch, ss_api, neigh, path):
        host_ip, host_mac, output_iface = self.get_conn_host_infos(neigh)
        if host_ip:
            neigh_mac = self.topo.node_to_node_mac(neigh, p4switch)
            output_iface = self.topo.node_to_node_port_num(p4switch, neigh)
            print('Add route via best',host_ip, neigh_mac, output_iface)
            ss_api.table_add('ipv4_lpm', 'set_nhop', [host_ip] ,[neigh_mac, str(output_iface)])

    def add_directly_conn_host(self, p4switch, ss_api):
        host_ip, host_mac, output_iface = self.get_conn_host_infos(p4switch)
        if host_ip:
            print('Add directly connected route ',host_ip,host_mac,output_iface)
            ss_api.table_add('ipv4_lpm', 'set_nhop', [host_ip] ,[host_mac, str(output_iface)])

    def route(self):
        """implement this function"""
        ecmp_group = {}
        for p4switch, ss_api in self.controllers.items():
            for neigh in self.topo.get_p4switches():
                if p4switch == neigh:
                    # Check if we have connected hosts
                    self.add_directly_conn_host(p4switch, ss_api)
                else:
                    shortest_path = self.topo.get_shortest_paths_between_nodes(p4switch, neigh)
                    if len(shortest_path) < 2:
                        # There is only 1 path
                        self.add_route_via_best(p4switch, ss_api, neigh, shortest_path)
                    else: 
                        # multipath
                        self.add_ecmp_group(p4switch, ss_api, neigh, shortest_path, ecmp_group)


            #print(self.topo.node(p4switch)['interfaces_to_node'])
            #for iface, neigh in self.topo.node(p4switch)['interfaces_to_node'].items():
            #    print(self.topo.node_to_node_port_num(p4switch, neigh)) 

    def main(self):
        self.route()


if __name__ == "__main__":
    controller = RoutingController().main()


'''topo.node('h1') #this also works topo['h1']
{u'gateway': u'10.1.1.1',
 u'interfaces_to_node': {u'h1-eth0': u's1'},
 u'interfaces_to_port': {u'h1-eth0': 0},
 u's1': {u'bw': None,
 u'delay': u'0ms',
 u'intf': u'h1-eth0',
 u'ip': u'10.1.1.2/24',
 u'mac': u'00:00:0a:01:01:02',
 u'queue_length': 1000,
 u'weight': 1},
 u'type': u'host'}
'''
