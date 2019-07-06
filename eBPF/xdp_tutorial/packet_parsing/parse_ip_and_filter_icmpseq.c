/* SPDX-License-Identifier: GPL-2.0 */
#include <stddef.h>
#include <linux/bpf.h>
#include <linux/in.h>
#include <linux/if_ether.h>
#include <linux/if_packet.h>
#include <linux/ip.h>
#include <linux/ipv6.h>
#include <linux/icmp.h>
#include <linux/icmpv6.h>
#include "bpf_helpers.h"
#include "bpf_endian.h"
/* Defines xdp_stats_map from packet04 */
#include "../common/xdp_stats_kern_user.h"
#include "../common/xdp_stats_kern.h"

#define bpf_printk(fmt, ...)                    \
({                              \
           char ____fmt[] = fmt;                \
           bpf_trace_printk(____fmt, sizeof(____fmt),   \
                ##__VA_ARGS__);         \
})

/* Header cursor to keep track of current parsing position */
struct hdr_cursor {
	void *pos;
};

/* Packet parsing helpers.
 *
 * Each helper parses a packet header, including doing bounds checking, and
 * returns the type of its contents if successful, and -1 otherwise.
 *
 * For Ethernet and IP headers, the content type is the type of the payload
 * (h_proto for Ethernet, nexthdr for IPv6), for ICMP it is the ICMP type field.
 * All return values are in host byte order.
 */
static __always_inline int parse_ethhdr(struct hdr_cursor *nh,
					void *data_end,
					struct ethhdr **ethhdr)
{
	struct ethhdr *eth = nh->pos;
	int hdrsize = sizeof(*eth);

	/* Byte-count bounds check; check if current pointer + size of header
	 * is after data_end.
	 */
	if (nh->pos + hdrsize > data_end)
		return -1;

	nh->pos += hdrsize;
	*ethhdr = eth;

	return bpf_ntohs(eth->h_proto);
}

/* Assignment 2: Implement and use this */
static __always_inline int parse_ip6hdr(struct hdr_cursor *nh,
					void *data_end,
					struct ipv6hdr **ip6hdr)
{
	struct ipv6hdr *v6hdr = nh->pos;
	if (v6hdr + 1 > data_end)
		return -1;
	nh->pos = v6hdr + 1;
	*ip6hdr = v6hdr;
	return bpf_htons(v6hdr->nexthdr);
}

/* Assignment 3: Implement and use this */
static __always_inline int parse_icmp6hdr(struct hdr_cursor *nh,
					  void *data_end,
					  struct icmp6hdr **icmp6hdr)
{
	struct icmp6hdr *icmpv6hdr = nh->pos;
	if (nh->pos + 1 > data_end)
		return -1;
	nh->pos += sizeof(*icmpv6hdr);
	*icmp6hdr = icmpv6hdr;
	return bpf_htons(icmpv6hdr->icmp6_sequence);
}

static __always_inline int parse_iphdr(struct hdr_cursor *nh,
					void *data_end,
					struct iphdr **ipheadr)
{

	struct iphdr *hdr = nh->pos;
	int hdrsize = hdr->ihl * 4;

	if (hdr + 1 > data_end)
		return -1;

	/* Variable-length IPv4 header, need to use byte-based arithmetic */
	//if (nh->pos + hdrsize > data_end)
		//return -1;

	nh->pos += hdrsize;
	*ipheadr = hdr;
	return hdr->protocol;
}

static __always_inline int parse_icmphdr(struct hdr_cursor *nh,
					  void *data_end,
					  struct icmphdr **icmphedr)
{
	struct icmphdr *icmpheadr = nh->pos;
	if (icmpheadr + 1 > data_end)
		return -1;
	nh->pos = icmpheadr + 1;
	*icmphedr = icmpheadr;
	return bpf_htons(icmpheadr->un.echo.sequence);
}

SEC("xdp_packet_parser")
int  xdp_parser_func(struct xdp_md *ctx)
{
	void *data_end = (void *)(long)ctx->data_end;
	void *data = (void *)(long)ctx->data;
	struct ethhdr *eth;

	/* Default action XDP_PASS, imply everything we couldn't parse, or that
	 * we don't want to deal with, we just pass up the stack and let the
	 * kernel deal with it.
	 */
	__u32 action = XDP_PASS; /* Default action */

        /* These keep track of the next header type and iterator pointer */
	struct hdr_cursor nh;
	int nh_type;

	/* Start next header cursor position at data start */
	nh.pos = data;

	/* Packet parsing in steps: Get each header one at a time, aborting if
	 * parsing fails. Each helper function does sanity checking (is the
	 * header type in the packet correct?), and bounds checking.
	 */
	nh_type = parse_ethhdr(&nh, data_end, &eth);
	if (nh_type != ETH_P_IPV6) {
		if (nh_type == ETH_P_IP){
			struct iphdr *ip;
			int proto;
			proto = parse_iphdr(&nh, data_end, &ip);
			bpf_printk("\nRETURN PROTO %d\n",proto);
			if (proto == IPPROTO_ICMP) {
				struct icmphdr *icmp;
				int icmp_seq = parse_icmphdr(&nh, data_end, &icmp);
				int even = icmp_seq % 2;
				bpf_printk("\n EVEN ?? %d and %d\n",even, icmp_seq);
				if (even != 0) {
					action = XDP_PASS;
					goto out;
				} else {
					action = XDP_DROP;
					goto out;
				}
			}
		}
		goto out;
	} else {
		struct ipv6hdr *ip6hdr;
		nh_type = parse_ip6hdr(&nh, data_end, &ip6hdr);
		if (nh_type == IPPROTO_ICMPV6) {
			struct icmp6hdr *icmpv6hdr;
			int icmp_seq = parse_icmp6hdr(&nh, data_end, &icmpv6hdr);
			if (icmp_seq % 2 != 0) {
				action = XDP_PASS;
				goto out;
			} else {
				action = XDP_DROP;
				goto out;
			}
		}
		goto out;
	}

	/* Assignment additions go below here */

	action = XDP_DROP;
out:
	return xdp_stats_record_action(ctx, action); /* read via xdp_stats */
}

char _license[] SEC("license") = "GPL";
