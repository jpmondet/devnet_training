/*************************************************************************
*********************** P A R S E R  *******************************
*************************************************************************/

parser MyParser(packet_in packet,
                out headers hdr,
                inout metadata meta,
                inout standard_metadata_t standard_metadata) {

    state start {
        //TODO 2: copy the parser from the previous exercise
        transition ethernet_parsing;
    }
    state ethernet_parsing {
    	packet.extract(hdr.ethernet);
    	transition select(hdr.ethernet.etherType) {
    		TYPE_IPV4: ip_parsing;
    		default: accept;
    	}
    }
    state ip_parsing {
    	packet.extract(hdr.ipv4);
    	transition select(hdr.ipv4.protocol) {
    		6: tcp_parsing;
    		default: accept;
    	}
    }
    state tcp_parsing {
    	packet.extract(hdr.tcp);
    	transition accept;
    }
}
/*************************************************************************
***********************  D E P A R S E R  *******************************
*************************************************************************/

control MyDeparser(packet_out packet, in headers hdr) {
    apply {
        //TODO 3: copy the deparser from the previous exercise
        packet.emit(hdr.ethernet);
        packet.emit(hdr.ipv4);
        packet.emit(hdr.tcp);
    }
}
