/* -*- P4_16 -*- */
#include <core.p4>
#include <v1model.p4>

/* CONSTANTS */
const bit<16> TYPE_IPV4 = 0x800;
const bit<8>  TYPE_TCP  = 6;

#define BLOOM_FILTER_ENTRIES 4096
#define BLOOM_FILTER_BIT_WIDTH 32
#define PACKET_THRESHOLD 1000

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

header ipv4_t {
    bit<4>    version;
    bit<4>    ihl;
    bit<8>    diffserv;
    bit<16>   totalLen;
    bit<16>   identification;
    bit<3>    flags;
    bit<13>   fragOffset;
    bit<8>    ttl;
    bit<8>    protocol;
    bit<16>   hdrChecksum;
    ip4Addr_t srcAddr;
    ip4Addr_t dstAddr;
}

header tcp_t{
    bit<16> srcPort;
    bit<16> dstPort;
    bit<32> seqNo;
    bit<32> ackNo;
    bit<4>  dataOffset;
    bit<4>  res;
    bit<1>  cwr;
    bit<1>  ece;
    bit<1>  urg;
    bit<1>  ack;
    bit<1>  psh;
    bit<1>  rst;
    bit<1>  syn;
    bit<1>  fin;
    bit<16> window;
    bit<16> checksum;
    bit<16> urgentPtr;
}

struct metadata {
    //TODO 7.1: define the 4 metadata fields you need for bloom filter index and reading the values
    bit<32> bf_index_h1;
    bit<32> bf_index_h2;
    bit<32> value1;
    bit<32> value2;
}

struct headers {
    ethernet_t   ethernet;
    ipv4_t       ipv4;
    tcp_t        tcp;
}

/*************************************************************************
*********************** P A R S E R  ***********************************
*************************************************************************/

parser MyParser(packet_in packet,
                out headers hdr,
                inout metadata meta,
                inout standard_metadata_t standard_metadata) {

    state start {
        //TODO 2: Define a parser for ethernet, ipv4 and tcp
        transition parse_ethernet;
    }
    state parse_ethernet {
        packet.extract(hdr.ethernet);
        transition select(hdr.ethernet.etherType) {
            TYPE_IPV4: parse_ipv4;
            default: accept;
        }
    }
    state parse_ipv4{
        packet.extract(hdr.ipv4);
        transition select(hdr.ipv4.protocol) {
            TYPE_TCP: parse_tcp;
            default: accept;
        }
    }
    state parse_tcp{
        packet.extract(hdr.tcp);
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


    //TODO 6: define the counting bloom filter using a register
    register<bit<32>>(4096) counting_bf;

    action drop() {
        mark_to_drop();
    }

    action update_bloom_filter(){
        //TODO 7: Define the update bloom filter action
        hash(meta.bf_index_h1, HashAlgorithm.crc16, (bit<1>)0, {
            hdr.ipv4.srcAddr,
            hdr.ipv4.dstAddr,
            hdr.tcp.srcPort,
            hdr.tcp.dstPort,
            hdr.ipv4.protocol
        }, (bit<16>)4096);
        hash(meta.bf_index_h2, HashAlgorithm.crc32, (bit<1>)0, {
            hdr.ipv4.srcAddr,
            hdr.ipv4.dstAddr,
            hdr.tcp.srcPort,
            hdr.tcp.dstPort,
            hdr.ipv4.protocol
        }, (bit<16>)4096);

        counting_bf.read(meta.value1, (bit<32>)meta.bf_index_h1);
        counting_bf.read(meta.value2, (bit<32>)meta.bf_index_h2);
        meta.value1 = meta.value1 + 1;
        meta.value2 = meta.value2 + 1;
        counting_bf.write((bit<32>)meta.bf_index_h1, meta.value1);
        counting_bf.write((bit<32>)meta.bf_index_h2, meta.value2);
    }

    action ipv4_forward(macAddr_t dstAddr, egressSpec_t port) {

        //TODO 5: implement the forwarding action
        hdr.ethernet.srcAddr = hdr.ethernet.dstAddr;
        hdr.ethernet.dstAddr = dstAddr;
        standard_metadata.egress_spec = port;
        hdr.ipv4.ttl = hdr.ipv4.ttl - 1;
    }

    table ipv4_lpm {
        //TODO 4: define the l3 forwarding table
        key = {
            hdr.ipv4.dstAddr: lpm;
        }
        actions = {
            ipv4_forward;
            drop;
            NoAction;
        }
        size = 1024;
        default_action = NoAction();
    }

    apply {
        //TODO 8: implement the main logic
        if (hdr.ipv4.isValid()) {
            if (hdr.tcp.isValid()) {
                update_bloom_filter();
                if (meta.value1 > PACKET_THRESHOLD && meta.value2 > PACKET_THRESHOLD) {
                    drop();
                } else {
                    ipv4_lpm.apply();
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
    apply {  }
}

/*************************************************************************
*************   C H E C K S U M    C O M P U T A T I O N   **************
*************************************************************************/

control MyComputeChecksum(inout headers hdr, inout metadata meta) {
    apply {
        //TODO 9: update the checksum field
        update_checksum(
            hdr.ipv4.isValid(),
            { hdr.ipv4.version,
              hdr.ipv4.ihl,
              hdr.ipv4.totalLen,
              hdr.ipv4.identification,
              hdr.ipv4.flags,
              hdr.ipv4.fragOffset,
              hdr.ipv4.ttl,
              hdr.ipv4.protocol,
              hdr.ipv4.srcAddr,
              hdr.ipv4.dstAddr },
            hdr.ipv4.hdrChecksum,
            HashAlgorithm.csum16
        );
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
