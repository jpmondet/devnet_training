/* -*- P4_16 -*- */
#include <core.p4>
#include <v1model.p4>

#include "include/headers.p4"
#include "include/parsers.p4"

/* CONSTANTS */
#define SKETCH_BUCKET_LENGTH 4
#define SKETCH_CELL_BIT_WIDTH 64 //Max counter size

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

    //TODO 4: define N registers
    register<bit<SKETCH_CELL_BIT_WIDTH>>(SKETCH_BUCKET_LENGTH) sketch0;
    register<bit<SKETCH_CELL_BIT_WIDTH>>(SKETCH_BUCKET_LENGTH) sketch1;
    register<bit<SKETCH_CELL_BIT_WIDTH>>(SKETCH_BUCKET_LENGTH) sketch2;
    register<bit<SKETCH_CELL_BIT_WIDTH>>(SKETCH_BUCKET_LENGTH) sketch3;

    action drop() {
        mark_to_drop();
    }

    //TODO 5: Define the sketch_count action
    action sketch_count() {
      //sketch0
      hash(meta.hash0, HashAlgorithm.crc32_custom, (bit<1>)0,
        { hdr.ipv4.srcAddr,
          hdr.ipv4.dstAddr,
          hdr.tcp.srcPort,
          hdr.tcp.dstPort,
          hdr.ipv4.protocol
        }, 
        (bit<32>)SKETCH_BUCKET_LENGTH); 
      sketch0.read(meta.reg_count0,(bit<32>)meta.hash0);
      meta.reg_count0 = meta.reg_count0 + 1;
      sketch0.write((bit<32>)meta.hash0, meta.reg_count0);

      //sketch1
      hash(meta.hash1, HashAlgorithm.crc32_custom, (bit<1>)0,
        { hdr.ipv4.srcAddr,
          hdr.ipv4.dstAddr,
          hdr.tcp.srcPort,
          hdr.tcp.dstPort,
          hdr.ipv4.protocol
        }, 
        (bit<32>)SKETCH_BUCKET_LENGTH); 
      sketch1.read(meta.reg_count1,(bit<32>)meta.hash1);
      meta.reg_count1 = meta.reg_count1 + 1;
      sketch1.write((bit<32>)meta.hash1, meta.reg_count1);

      //sketch2
      hash(meta.hash2, HashAlgorithm.crc32_custom, (bit<1>)0,
        { hdr.ipv4.srcAddr,
          hdr.ipv4.dstAddr,
          hdr.tcp.srcPort,
          hdr.tcp.dstPort,
          hdr.ipv4.protocol
        }, 
        (bit<32>)SKETCH_BUCKET_LENGTH); 
      sketch2.read(meta.reg_count2,(bit<32>)meta.hash2);
      meta.reg_count2 = meta.reg_count2 + 1;
      sketch2.write((bit<32>)meta.hash2, meta.reg_count2);

      //sketch3
      hash(meta.hash3, HashAlgorithm.crc32_custom, (bit<1>)0,
        { hdr.ipv4.srcAddr,
          hdr.ipv4.dstAddr,
          hdr.tcp.srcPort,
          hdr.tcp.dstPort,
          hdr.ipv4.protocol
        }, 
        (bit<32>)SKETCH_BUCKET_LENGTH); 
      sketch3.read(meta.reg_count3,(bit<32>)meta.hash3);
      meta.reg_count3 = meta.reg_count3 + 1;
      sketch3.write((bit<32>)meta.hash3, meta.reg_count3);
    }

    //TODO 1: define the forwarding table
    //TODO 2: define the set_egress_port action
    action set_egress_port(bit<9> egress_port){
      standard_metadata.egress_spec = egress_port;
    }
    table forwarding {
      key = {
        standard_metadata.ingress_port: exact;
      }
      actions = {
        set_egress_port;
        drop;
      }
      size = 64;
      default_action = drop;
    }


    apply {
        //TODO 6: define the pipeline logic
        if(hdr.ipv4.isValid()) {
          if(hdr.tcp.isValid()) {
            sketch_count();
          }
        }
        forwarding.apply();
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
