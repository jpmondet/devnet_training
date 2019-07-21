# XDP reminders


| Struct            | Header file          |
|-------------------+----------------------|
| =struct ethhdr=   | =<linux/if_ether.h>= |
| =struct ipv6hdr=  | =<linux/ipv6.h>=     |
| =struct iphdr=    | =<linux/ip.h>=       |
| =struct icmp6hdr= | =<linux/icmpv6.h>=   |
| =struct icmphdr=  | =<linux/icmp.h>=     |

11 registers including : 
  * r0 to store return values
  * r1 to r5 (used as function call arguments -> Thus 5 arguments MAX per function call)
  * r6 to r9 
  * r10 (read-only)

## Debugging 

Very useful macro to be able to print variables on the BPF program.
```c
#define bpf_printk(fmt, ...)                    \
({                              \
           char ____fmt[] = fmt;                \
           bpf_trace_printk(____fmt, sizeof(____fmt),   \
                ##__VA_ARGS__);         \
})
```
The ouput can be seen on `/sys/kernel/debug/tracing/trace_pipe`

## Catches 

- Misleading type cast to please the compiler on packet infos : 

```c
struct xdp_md {
	__u32 data;
	__u32 data_end;
	__u32 data_meta;
	/* Below access go through struct xdp_rxq_info */
	__u32 ingress_ifindex; /* rxq->dev->ifindex */
	__u32 rx_queue_index;  /* rxq->queue_index  */
};
```

```c
	void *data_end = (void *)(long)ctx->data_end;
	void *data = (void *)(long)ctx->data;
```

- "The bpf_redirect helper actually shouldn't be used in production as it is slow and can't be configured from user space." (@xdp-tutorial)

