/*************************************************************************
*********************** P A R S E R  *******************************
*************************************************************************/

parser MyParser(packet_in packet,
                out headers hdr,
                inout metadata meta,
                inout standard_metadata_t standard_metadata) {

    state start {
        //TODO 2: Define a parser for ethernet, ipv4 and tcp
        transition eth_parser;
    }
    state eth_parser {
    	packet.extract(hdr.ethernet);
		transition select(hdr.ethernet.etherType) {
			TYPE_IPV4: ip_parser;
			default: accept;
		}
    }
    state ip_parser {
    	packet.extract(hdr.ipv4);
    	transition select(hdr.ipv4.protocol) {
    		6: tcp_parser;
    		default: accept;
    	}
    }
    state tcp_parser {
    	packet.extract(hdr.tcp);
    	transition accept;
    }
}

/*************************************************************************
***********************  D E P A R S E R  *******************************
*************************************************************************/

control MyDeparser(packet_out packet, in headers hdr) {
    apply {
        //TODO 3: Deparse the ethernet, ipv4 and tcp headers
        packet.emit(hdr.ethernet);
        packet.emit(hdr.ipv4);
        packet.emit(hdr.tcp);
    }
}
