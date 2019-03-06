/* -*- P4_16 -*- */
#include <core.p4>
#include <v1model.p4>

//My includes
#include "include/headers.p4"
#include "include/parsers.p4"

#define PKT_INSTANCE_TYPE_NORMAL 0
#define PKT_INSTANCE_TYPE_INGRESS_CLONE 1
#define PKT_INSTANCE_TYPE_EGRESS_CLONE 2
#define PKT_INSTANCE_TYPE_COALESCED 3
#define PKT_INSTANCE_TYPE_INGRESS_RECIRC 4
#define PKT_INSTANCE_TYPE_REPLICATION 5
#define PKT_INSTANCE_TYPE_RESUBMIT 6

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

    action ecmp_group(bit<14> ecmp_group_id, bit<16> num_nhops){
        hash(meta.ecmp_hash,
	    HashAlgorithm.crc16,
	    (bit<1>)0,
	    { hdr.ipv4.srcAddr,
	      hdr.ipv4.dstAddr,
          hdr.tcp.srcPort,
          hdr.tcp.dstPort,
          hdr.ipv4.protocol},
	    num_nhops);

	    meta.ecmp_group_id = ecmp_group_id;
    }

    action set_nhop(macAddr_t dstAddr, egressSpec_t port) {

        //set the src mac address as the previous dst, this is not correct right?
        hdr.ethernet.srcAddr = hdr.ethernet.dstAddr;

       //set the destination mac address that we got from the match in the table
        hdr.ethernet.dstAddr = dstAddr;

        //set the output port that we also get from the table
        standard_metadata.egress_spec = port;

        //decrease ttl by 1
        hdr.ipv4.ttl = hdr.ipv4.ttl - 1;
    }

    table ecmp_group_to_nhop {
        key = {
            meta.ecmp_group_id:    exact;
            meta.ecmp_hash: exact;
        }
        actions = {
            drop;
            set_nhop;
        }
        size = 1024;
    }

    table ipv4_lpm {
        key = {
            hdr.ipv4.dstAddr: lpm;
        }
        actions = {
            set_nhop;
            ecmp_group;
            drop;
        }
        size = 1024;
        default_action = drop;
    }

    action set_next_device(bit<32> device) {
      meta.device = device;
    }

    table attached_device {
      key = {
        standard_metadata.egress_spec: exact;
      }
      actions = {
        set_next_device;
        NoAction;
      }
      default_action = NoAction;
      size = 64;
    }
    apply {

        if (standard_metadata.instance_type == PKT_INSTANCE_TYPE_INGRESS_RECIRC){
            bit<32> src_ip = hdr.ipv4.srcAddr;
            hdr.ipv4.srcAddr = hdr.ipv4.dstAddr;
            hdr.ipv4.dstAddr = src_ip;
            hdr.ethernet.etherType = 0x7778;
        }

        if (hdr.ipv4.isValid()){
            switch (ipv4_lpm.apply().action_run){
                ecmp_group: {
                    ecmp_group_to_nhop.apply();
                }
            }
        }

        attached_device.apply();

    }
}

/*************************************************************************
****************  E G R E S S   P R O C E S S I N G   *******************
*************************************************************************/

control MyEgress(inout headers hdr,
                 inout metadata meta,
                 inout standard_metadata_t standard_metadata) {
    
    register<bit<48>>(1024) notif_time_stamp;

    action read_notif_register(){
      
      hash(meta.notif_id,
        HashAlgorithm.crc16,
        (bit<1>)0,
        { 
          hdr.ipv4.srcAddr,
          hdr.ipv4.dstAddr,
          hdr.tcp.srcPort,
          hdr.tcp.dstPort,
          hdr.ipv4.protocol
        },
        (bit<12>)1024);
      
      notif_time_stamp.read(meta.notif_last_timestamp, (bit<32>)meta.notif_id);
    }

    apply {

      if (standard_metadata.instance_type == PKT_INSTANCE_TYPE_EGRESS_CLONE) {
        recirculate(meta.recirc);
      } else {

        if (standard_metadata.instance_type == PKT_INSTANCE_TYPE_NORMAL && hdr.ethernet.etherType != 0x7778) {


          if (hdr.tcp.isValid()){
            if (hdr.telemetry.isValid()){
              if ( hdr.telemetry.enq_qdepth < (bit<16>)standard_metadata.enq_qdepth) {
                hdr.telemetry.enq_qdepth = (bit<16>)standard_metadata.enq_qdepth;
              }
              if (meta.device != 2) {
                if (hdr.telemetry.enq_qdepth > 30) {
                  read_notif_register();
                  if (standard_metadata.ingress_global_timestamp - meta.notif_last_timestamp > 48w1000000){
                    bit<8> redirect;
                    random(redirect, 8w0, 8w10);
                    if (redirect < 4) {
                      clone(CloneType.E2E, 64);
                    }
                  }
                }
                hdr.telemetry.setInvalid();
                hdr.ethernet.etherType = TYPE_IPV4;
              }
            } else {
              if (meta.device == 2) {
                hdr.telemetry.setValid();
                hdr.telemetry.enq_qdepth = (bit<16>)standard_metadata.enq_qdepth;
                hdr.ethernet.etherType = TYPE_TELEMETRY;
                hdr.telemetry.nextHeaderType = TYPE_IPV4;
              }
            }
          }
       }
    }
  }
}

/*************************************************************************
*************   C H E C K S U M    C O M P U T A T I O N   **************
*************************************************************************/

control MyComputeChecksum(inout headers hdr, inout metadata meta) {
     apply {
	update_checksum(
	    hdr.ipv4.isValid(),
            { hdr.ipv4.version,
	          hdr.ipv4.ihl,
              hdr.ipv4.dscp,
              hdr.ipv4.ecn,
              hdr.ipv4.totalLen,
              hdr.ipv4.identification,
              hdr.ipv4.flags,
              hdr.ipv4.fragOffset,
              hdr.ipv4.ttl,
              hdr.ipv4.protocol,
              hdr.ipv4.srcAddr,
              hdr.ipv4.dstAddr },
              hdr.ipv4.hdrChecksum,
              HashAlgorithm.csum16);
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
