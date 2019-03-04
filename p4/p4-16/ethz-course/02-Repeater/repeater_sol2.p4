/* -*- P4_16 -*- */
#include <core.p4>
#include <v1model.p4>

/*************************************************************************
*********************** H E A D E R S  ***********************************
*************************************************************************/

struct metadata {
}

struct headers {
}

/*************************************************************************
*********************** P A R S E R  ***********************************
*************************************************************************/

parser MyParser(packet_in packet,
                out headers hdr,
                inout metadata meta,
                inout standard_metadata_t standard_metadata) {

      state start{
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

    /* TODO 1: For solution 2 -> define a table that matches standard_metadata.ingress_port */
    /* TODO 2: For solution 2 -> define an action that modifies the egress_port */

    // THE TABLE MUST BE FILLED VIA CLI IN ORDER TO BE USED
    // simple_switch_CLI --thrift-port 9090
    // table_add MyIngress.match_ingr MyIngree.repeat 1 => 2
    // table_add MyIngress.match_ingr MyIngree.repeat 2 => 1
    // (can also be put in a file and added directly on the cli)
    action repeat(bit<9> egr_port){
        standard_metadata.egress_spec = egr_port;
    }
    table match_ingr {
        key = {
            standard_metadata.ingress_port: exact;
        }
        actions = {
            repeat;
            NoAction;
        }
        size = 2;
        default_action = NoAction;
    }
    apply {
        /* TODO 3:*/
        /* Solution 1: Without tables, write the algorithm directly here*/
        /* Solution 2: Apply the table you use */
        match_ingr.apply()
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

control MyComputeChecksum(inout headers  hdr, inout metadata meta) {
    apply { }
}

/*************************************************************************
***********************  D E P A R S E R  *******************************
*************************************************************************/

control MyDeparser(packet_out packet, in headers hdr) {
    apply {

    /* Deparser not needed */

    }
}

/*************************************************************************
***********************  S W I T C H  *******************************
*************************************************************************/

V1Switch(
MyParser(),
MyVerifyChecksum(),
MyIngress(),
MyEgress(),
MyComputeChecksum(),
MyDeparser()
) main;