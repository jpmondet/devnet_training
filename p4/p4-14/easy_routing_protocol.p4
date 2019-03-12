/*
Copyright 2013-present Barefoot Networks, Inc. 

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/

// TODO: define headers & header instances

header_type easyroute_fixed_t {
	fields {
		preamble: 64;
		num_valid: 32;
	}
}

header easyroute_fixed_t easyroute_fixed;

header_type easyroute_stack_t {
	fields {
		port: 8;
	}
}

header easyroute_stack_t easyroute_stack;

parser start {
    // TODO
    return select(current(0,64)) {
    	0: parse_fixed;
    	default: ingress;
    }
}
parser parse_fixed {
	extract(easyroute_fixed);
	return select(latest.num_valid){
		0: ingress;
		default: parse_stack;
	}
}

parser parse_stack {
	extract(easyroute_stack);
	return ingress;
}

// TODO: define parser states

action _drop() {
    drop();
}

action route() {
    /* modify_field(standard_metadata.egress_spec,  TODO: port field from your header );*/
    // TODO: update your header
    modify_field(standard_metadata.egress_spec, easyroute_stack.port);
    add_to_field(easyroute_fixed.num_valid, -1);
    remove_header(easyroute_stack);
}

table fib {
	reads {
		easyroute_stack: valid;
	}
	actions{
		_drop;
		route;
	}
	size: 10;
}

control ingress {
    // TODO
    apply(fib);
}

control egress {
    // leave empty
}

