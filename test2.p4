#include <core.p4>
#include <v1model.p4>

header ethernet_t {
    bit<48> dst_addr;
    bit<48> src_addr;
}

struct Headers {
    ethernet_t eth_hdr;
}

struct Meta {}

parser myparser(packet_in pkt, out Headers hdr
	, inout Meta m, inout standard_metadata_t sm) {
    state start {
        pkt.extract(hdr.eth_hdr);
        transition accept;
    }
}

control ingress(inout Headers h, inout Meta m, 
	inout standard_metadata_t sm) {
    action modify() {
        h.eth_hdr.src_addr = h.eth_hdr.dst_addr;
    }
    table simple_table {
        actions = {
            modify();
        }
    }
    apply {
        simple_table.apply();
    }
}

control checksum(inout Headers h, inout Meta m) {apply{}}
control update(inout Headers h, inout Meta m) {apply{}}
control egress(inout Headers h, inout Meta m, inout standard_metadata_t sm) {apply{}}
control deparser(packet_out b, in Headers h) { apply {b.emit(h);} }

V1Switch(myparser(), checksum(), ingress(), egress(), update(), deparser()) main;

