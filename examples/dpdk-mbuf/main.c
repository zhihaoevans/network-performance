/* Minimal EAL + mempool + mbuf lifecycle exercise; no network I/O. */
#include <stdio.h>
#include <string.h>
#include <rte_eal.h>
#include <rte_errno.h>
#include <rte_mbuf.h>
#include <rte_mempool.h>

int main(int argc, char **argv)
{
    if (rte_eal_init(argc, argv) < 0) {
        fprintf(stderr, "EAL init failed\n");
        return 1;
    }
    struct rte_mempool *pool = rte_pktmbuf_pool_create(
        "learning_pool", 1023, 0, 0, RTE_MBUF_DEFAULT_BUF_SIZE, SOCKET_ID_ANY);
    if (pool == NULL) {
        fprintf(stderr, "mempool: %s\n", rte_strerror(rte_errno));
        rte_eal_cleanup();
        return 1;
    }
    unsigned before = rte_mempool_avail_count(pool);
    struct rte_mbuf *packet = rte_pktmbuf_alloc(pool);
    if (packet == NULL) {
        fprintf(stderr, "mbuf allocation failed\n");
        rte_mempool_free(pool);
        rte_eal_cleanup();
        return 1;
    }
    const char payload[] = "hello DPDK";
    char *dst = rte_pktmbuf_append(packet, sizeof(payload));
    if (dst == NULL) {
        fprintf(stderr, "not enough tailroom\n");
        rte_pktmbuf_free(packet);
        rte_mempool_free(pool);
        rte_eal_cleanup();
        return 1;
    }
    memcpy(dst, payload, sizeof(payload));
    printf("payload=%s pkt_len=%u data_len=%u segments=%u\n",
           rte_pktmbuf_mtod(packet, const char *),
           (unsigned)packet->pkt_len, (unsigned)packet->data_len,
           (unsigned)packet->nb_segs);
    rte_pktmbuf_free(packet);
    unsigned after = rte_mempool_avail_count(pool);
    printf("pool before=%u after=%u\n", before, after);
    rte_mempool_free(pool);
    int cleaned = rte_eal_cleanup();
    if (before != after || cleaned != 0) {
        fprintf(stderr, "resource lifecycle check failed\n");
        return 1;
    }
    puts("PASS: mbuf returned to pool");
    return 0;
}
