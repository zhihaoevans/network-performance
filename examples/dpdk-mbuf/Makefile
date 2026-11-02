CC ?= cc
PKG_CONFIG ?= pkg-config
CFLAGS += -O2 -g -Wall -Wextra
DPDK_CFLAGS := $(shell $(PKG_CONFIG) --cflags libdpdk)
DPDK_LIBS := $(shell $(PKG_CONFIG) --libs libdpdk)

.PHONY: all clean check-deps
all: build/mbuf-demo

check-deps:
	$(PKG_CONFIG) --exists libdpdk

build/mbuf-demo: main.c | check-deps
	mkdir -p build
	$(CC) $(CFLAGS) $(DPDK_CFLAGS) $< -o $@ $(DPDK_LIBS)

clean:
	rm -f build/mbuf-demo
