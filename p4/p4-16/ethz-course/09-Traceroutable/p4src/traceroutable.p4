/* -*- P4_16 -*- */
#include <core.p4>
#include <v1model.p4>

//My includes
#include "include/headers.p4"
#include "include/parsers.p4"

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

    //TODO 1: define the icmp_ingress_port table and the set_src_icmp_ip action

    action set_src_icmp_ip(ip4Addr_t ipAddr) {
      hdr.ipv4_icmp.srcAddr = ipAddr;
    }

    table icmp_ingress_port {
      key = {
        standard_metadata.ingress_port: exact;
      }
      actions = {
        set_src_icmp_ip;
        NoAction;
      }
      default_action = NoAction;
      size=64;
    }

    apply {

        //TODO 4: check that the ttl is > 1
        if (hdr.ipv4.ttl > 1) {
          if (hdr.ipv4.isValid()){
              switch (ipv4_lpm.apply().action_run){
                  ecmp_group: {
                      ecmp_group_to_nhop.apply();
                  }
              }
          }

        //Traceroute Logic (only for TCP probes)
        //TODO 5: implement the ICMP generation logic
        } else if (hdr.ipv4.ttl == 1) {
            if (hdr.ipv4.isValid()){
              if (hdr.tcp.isValid()){
                hdr.ipv4_icmp.setValid();
                hdr.icmp.setValid();
                standard_metadata.egress_spec = standard_metadata.ingress_port;
                bit<48> tmpAddr =  hdr.ethernet.srcAddr;
                hdr.ethernet.srcAddr = hdr.ethernet.dstAddr;
                hdr.ethernet.dstAddr = tmpAddr;
                hdr.ipv4_icmp = hdr.ipv4;
                hdr.ipv4_icmp.dstAddr = hdr.ipv4.srcAddr;
                icmp_ingress_port.apply();
                hdr.ipv4_icmp.protocol = 1;
                hdr.ipv4_icmp.ttl = 255;
                hdr.ipv4_icmp.totalLen = 56;
                hdr.icmp.icmpType = 11;
                hdr.icmp.code = 0;
                truncate((bit<32>)70);
              }
            }
          }
        
    }
}

/*************************************************************************
****************  E G R E S S   P R O C E S S I N G   *******************
*************************************************************************/

control MyEgress(inout headers hdr,
                 inout metadata meta,
                 inout standard_metadata_t standard_metadata) {
    apply {

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

     //TODO 6: define the checksums for the new two headers ipv4_icmp and icmp
  update_checksum(
    hdr.ipv4_icmp.isValid(),
        { hdr.ipv4_icmp.version,
          hdr.ipv4_icmp.ihl,
          hdr.ipv4_icmp.dscp,
          hdr.ipv4_icmp.ecn,
          hdr.ipv4_icmp.totalLen,
          hdr.ipv4_icmp.identification,
          hdr.ipv4_icmp.flags,
          hdr.ipv4_icmp.fragOffset,
          hdr.ipv4_icmp.ttl,
          hdr.ipv4_icmp.protocol,
          hdr.ipv4_icmp.srcAddr,
          hdr.ipv4_icmp.dstAddr },
          hdr.ipv4_icmp.hdrChecksum,
          HashAlgorithm.csum16);

  update_checksum(
    hdr.icmp.isValid(),
        { hdr.icmp.icmpType,
          hdr.icmp.code,
          hdr.icmp.unused,
          hdr.ipv4.version,
          hdr.ipv4.ihl,
          hdr.ipv4.dscp,
          hdr.ipv4.ecn,
          hdr.ipv4.totalLen,
          hdr.ipv4.identification,
          hdr.ipv4.flags,
          hdr.ipv4.fragOffset,
          hdr.ipv4.ttl,
          hdr.ipv4.protocol,
          hdr.ipv4.hdrChecksum,
          hdr.ipv4.srcAddr,
          hdr.ipv4.dstAddr,
          hdr.tcp.srcPort,
          hdr.tcp.dstPort,
          hdr.tcp.seqNo
          },
          hdr.icmp.checksum,
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
