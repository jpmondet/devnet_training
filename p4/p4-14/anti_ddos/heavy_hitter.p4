/* Copyright 2013-present Barefoot Networks, Inc.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#include "includes/headers.p4"
#include "includes/parser.p4"

// TODO: Define the threshold value
#define HH_THRESHOLD 10

field_list ipv4_checksum_list {
        ipv4.version;
        ipv4.ihl;
        ipv4.diffserv;
        ipv4.totalLen;
        ipv4.identification;
        ipv4.flags;
        ipv4.fragOffset;
        ipv4.ttl;
        ipv4.protocol;
        ipv4.srcAddr;
        ipv4.dstAddr;
}

field_list_calculation ipv4_checksum {
    input {
        ipv4_checksum_list;
    }
    algorithm : csum16;
    output_width : 16;
}

calculated_field ipv4.hdrChecksum  {
    verify ipv4_checksum;
    update ipv4_checksum;
}

action _drop() {
    drop();
}

header_type custom_metadata_t {
    fields {
        nhop_ipv4: 32;
        // TODO: Add the metadata for hash indices and count values
        hash_1: 16;
        hash_2: 16;
        count_1: 16;
        count_2: 16;
    }
}

metadata custom_metadata_t custom_metadata;

action set_nhop(nhop_ipv4, port) {
    modify_field(custom_metadata.nhop_ipv4, nhop_ipv4);
    modify_field(standard_metadata.egress_spec, port);
    add_to_field(ipv4.ttl, -1);
}

action set_dmac(dmac) {
    modify_field(ethernet.dstAddr, dmac);
}

// TODO: Define the field list to compute the hash on
// Use the 5 tuple of 
// (src ip, dst ip, src port, dst port, ip protocol)

field_list five_tuples_field_list {
        ipv4.protocol;
        ipv4.srcAddr;
        ipv4.dstAddr;
        tcp.srcPort;
        tcp.dstPort;
}

// TODO: Define two different hash functions to store the counts
// Note: Please use csum16 and crc16 for the hash functions

field_list_calculation hash_count_1 {
    input {
        five_tuples_field_list;
    }
    algorithm : csum16;
    output_width : 16;
}

field_list_calculation hash_count_2 {
    input {
        five_tuples_field_list;
    }
    algorithm : crc16;
    output_width : 16;
}

// TODO: Define the registers to store the counts

register hh_counter_1 {
    width : 16;
    instance_count : 16;
}

register hh_counter_2 {
    width : 16;
    instance_count : 16;
}

// TODO: Actions to set heavy hitter filter

action set_hh_filter() {
    modify_field_with_hash_based_offset(custom_metadata.hash_1, 0,
                                        hash_count_1, 16);
    register_read(custom_metadata.count_1, hh_counter_1, custom_metadata.hash_1);
    add_to_field(custom_metadata.count_1, 1);
    register_write(hh_counter_1, custom_metadata.hash_1, custom_metadata.count_1);

    modify_field_with_hash_based_offset(custom_metadata.hash_2, 0,
                                        hash_count_2, 16);
    register_read(custom_metadata.count_2, hh_counter_2, custom_metadata.hash_2);
    add_to_field(custom_metadata.count_2, 1);
    register_write(hh_counter_2, custom_metadata.hash_2, custom_metadata.count_2);    
}


// TODO: Define the tables to run actions'

table set_hh_counters_table {
    actions {
        set_hh_filter;
    }
    size: 1;
}


// TODO: Define table to drop the heavy hitter traffic

table drop_hh_table {
    actions {
        _drop;
    }
    size: 1;
}


table ipv4_lpm {
    reads {
        ipv4.dstAddr : lpm;
    }
    actions {
        set_nhop;
        _drop;
    }
    size: 1024;
}

table forward {
    reads {
        custom_metadata.nhop_ipv4 : exact;
    }
    actions {
        set_dmac;
        _drop;
    }
    size: 512;
}

action rewrite_mac(smac) {
    modify_field(ethernet.srcAddr, smac);
}

table send_frame {
    reads {
        standard_metadata.egress_port: exact;
    }
    actions {
        rewrite_mac;
        _drop;
    }
    size: 256;
}

control ingress {
    // TODO: Add table control here
    apply(set_hh_counters_table);
    if (custom_metadata.count_1 >= HH_THRESHOLD and custom_metadata.count_2 >= HH_THRESHOLD) {
        apply(drop_hh_table);
    } else {
        apply(ipv4_lpm);
        apply(forward);
    }
}

control egress {
    apply(send_frame);
}

