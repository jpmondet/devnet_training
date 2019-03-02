/* -*- P4_16 -*- */
#include <core.p4>
#include <v1model.p4>

const bit<16> TYPE_IPV4 = 0x800;
const bit<16> TYPE_BROADCAST = 0x1234;

/*************************************************************************
*********************** H E A D E R S  ***********************************
*************************************************************************/

typedef bit<9>  egressSpec_t;
typedef bit<48> macAddr_t;
typedef bit<32> ip4Addr_t;

header ethernet_t {
    macAddr_t dstAddr;
    macAddr_t srcAddr;
    bit<16>   etherType;
}

//TODO 2: define the learn_t struct that you will digest

struct learn_t {
    macAddr_t srcAddr;
    bit<16> ingr_port;
}

struct metadata {
    /* empty */
    //TODO 3: declare one learn_t variable
    learn_t learned;
}

struct headers {
    ethernet_t   ethernet;
}


/*************************************************************************
*********************** P A R S E R  ***********************************
*************************************************************************/

parser MyParser(packet_in packet,
                out headers hdr,
                inout metadata meta,
                inout standard_metadata_t standard_metadata) {

    state start {
        packet.extract(hdr.ethernet);
        transition accept;
    }
}


/*************************************************************************
************   C H E C K S U M    V E R I F I C A T I O N   *************
*************************************************************************/

control MyVerifyChecksum(inout headers hdr, inout metadata meta) {
    apply {  }
}


/*************************************************************************
**************  I N G R E S S   P R O C E S S I N G   *******************
*************************************************************************/

control MyIngress(inout headers hdr,
                  inout metadata meta,
                  inout standard_metadata_t standard_metadata) {

    action drop() {

        mark_to_drop();
    }

    //TODO 4: copy the ingress code from the previous exercise. Modify the `mac_learn` action so now it digest the learn metadata
    // struct you defined.

    action forward(bit<9> egress_port){
        standard_metadata.egress_spec = egress_port;
    }

    table dmac {
        key = {
            hdr.ethernet.dstAddr: exact;
        }
        actions = {
            forward;
            NoAction;
        }
        size = 512;
        default_action = NoAction;
    }

    action set_mcast_grp(bit<16> mcast_group){
        standard_metadata.mcast_grp = mcast_group;
    }
    table broadcast {
        key = {
            standard_metadata.ingress_port: exact;
        }
        actions = {
            set_mcast_grp;
            NoAction;
        }
        default_action = NoAction;
        size = 256;
    }

    action mac_learn(){
        meta.learned.srcAddr = hdr.ethernet.srcAddr;
        meta.learned.ingr_port = (bit<16>)standard_metadata.ingress_port;
        digest(1,meta.learned);
    }
    table smac {
        key = {
            hdr.ethernet.srcAddr: exact;    
        }
        actions = {
            mac_learn;
            NoAction;
        }
        default_action = mac_learn();
        size = 512;
    }


    apply {
        //TODO 5: copy the logic from the previous exercise
        smac.apply();
        if (dmac.apply().hit) {

        } else {
            broadcast.apply();
        }
    }
}

/*************************************************************************
****************  E G R E S S   P R O C E S S I N G   *******************
*************************************************************************/

control MyEgress(inout headers hdr,
                 inout metadata meta,
                 inout standard_metadata_t standard_metadata) {


    apply {  }
}

/*************************************************************************
*************   C H E C K S U M    C O M P U T A T I O N   **************
*************************************************************************/

control MyComputeChecksum(inout headers hdr, inout metadata meta) {
     apply {

    }
}


/*************************************************************************
***********************  D E P A R S E R  *******************************
*************************************************************************/

control MyDeparser(packet_out packet, in headers hdr) {
    apply {
        //parsed headers have to be added again into the packet.
        packet.emit(hdr.ethernet);
    }
}

/*************************************************************************
***********************  S W I T C H  *******************************
*************************************************************************/

//switch architecture
V1Switch(
MyParser(),
MyVerifyChecksum(),
MyIngress(),
MyEgress(),
MyComputeChecksum(),
MyDeparser()
) main;
