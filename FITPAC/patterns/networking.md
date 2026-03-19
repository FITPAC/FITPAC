# Networking & Communication (Compressed)
# ID: networking
# Module key (for fragment IDs): `networking` (see `master_index.yaml.pattern_map`)
# Version: 1.0.0
# Status: active
# Last reviewed: 2026-02-23
# Assumptions: Boundaries governs contracts; security governs trust; this governs transport and protocol semantics.
# License: CC-BY-4.0
# License URL: https://creativecommons.org/licenses/by/4.0/
# Origin: maintainer
# Adoption Status: adopted
# Standard Inclusion: canonical-reference
# Canonical Manifest Pin: FITPAC 1.0.0 reference distribution

## p1: Protocol Selection Contract
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: networking
category: other
```

- Primitives: Protocol (HTTP, gRPC, WebSocket, TCP, UDP), ProtocolProfile (latency, throughput, reliability, bidirectional).
- Invariants: Protocol MUST match communication requirements (networking.inv.1).
- Triggers: protocol_mismatch, performance_degradation.
- RULE: Select protocol based on: request-response vs streaming, latency sensitivity, payload size, browser compatibility. HTTP: universal, cacheable. gRPC: efficient, typed. WebSocket: bidirectional, real-time. Document protocol choice rationale.

## p2: Connection Lifecycle
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: networking
category: other
```

- Primitives: Connection (state, idle_timeout, max_age), ConnectionPool (size, acquire_timeout).
- Invariants: Connections MUST be returned to pool or closed (networking.inv.2).
- Triggers: connection_leak, pool_exhaustion.
- RULE: Use ConnectionPool for connection reuse. Configure: pool size, acquire timeout, idle timeout, max connection age. Validate connections before use. Close stale connections. Monitor pool metrics. Handle exhaustion gracefully.

## p3: Load Balancing Contract
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: networking
category: other
```

- Primitives: LoadBalancer (algorithm, health_check), BalancingAlgorithm (round_robin, least_connections, weighted, consistent_hash).
- Invariants: Traffic MUST NOT route to unhealthy instances (networking.inv.3).
- Triggers: instance_unhealthy, uneven_distribution.
- RULE: Select BalancingAlgorithm based on: stateless (round-robin), session affinity (consistent-hash), resource-aware (least-connections). Configure health checks. Handle instance failures. Monitor distribution evenness.

## p4: Service Discovery Contract
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: networking
category: other
```

- Primitives: ServiceEndpoint (host, port, metadata), DiscoveryClient, RegistrationTTL.
- Invariants: Stale registrations MUST expire within TTL (networking.inv.4).
- Triggers: service_not_found, stale_endpoint.
- RULE: Services register with discovery system. Clients query for endpoints. Handle: no instances found, all instances unhealthy, discovery system unavailable. Cache with appropriate TTL. Extends `distributed_systems.p8`.

## p5: DNS Contract
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: networking
category: other
```

- Primitives: DNSRecord (type, TTL, value), DNSResolution, DNSCaching.
- Invariants: DNS TTL MUST be honored for caching (networking.inv.5).
- Triggers: dns_resolution_failed, stale_dns.
- RULE: Use appropriate DNS record types. Set TTL based on change frequency. Handle: DNS failures, negative caching, TTL expiration. For service discovery, consider low TTL or alternatives. Monitor DNS latency.

## p6: TLS/mTLS Contract
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: networking
category: other
```

- Primitives: TLSConfig (min_version, cipher_suites, certificate), mTLSConfig (client_cert_required).
- Invariants: Connections MUST use TLS >= declared minimum version (networking.inv.6).
- Triggers: tls_handshake_failed, certificate_expired, insecure_connection.
- RULE: Enforce TLS for all external connections. Configure minimum TLS version (1.2+). Select secure cipher suites. mTLS for service-to-service. Monitor certificate expiration. Rotate certificates before expiry.

## p7: Retry and Backoff
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: networking
category: other
```

- Primitives: RetryPolicy (max_attempts, backoff_strategy, retryable_errors), BackoffStrategy (fixed, exponential, jittered).
- Invariants: Retries MUST NOT exceed configured attempts (networking.inv.7).
- Triggers: retry_exhausted, retry_storm.
- RULE: Define retryable errors (transient: 503, timeout; not retryable: 400, 404). Use exponential backoff with jitter to prevent thundering herd. Set circuit breaker to prevent retry storms (resilience.p1). Extends boundaries.p3.

## p8: Timeout Hierarchy
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: networking
category: other
```

- Primitives: ConnectTimeout, ReadTimeout, WriteTimeout, TotalTimeout.
- Invariants: ConnectTimeout + ReadTimeout MUST NOT exceed caller's deadline (networking.inv.8).
- Triggers: timeout_exceeded, hung_connection.
- RULE: Configure timeout layers: connection establishment, individual read/write, total request. Propagate caller deadline minus processing buffer. Log timeout events with context. Shorter timeouts for health checks.

## p9: Keep-Alive and Heartbeat
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: networking
category: other
```

- Primitives: KeepAliveConfig (interval, timeout, probes), Heartbeat.
- Triggers: connection_stale, heartbeat_missed.
- RULE: Enable keep-alive for long-lived connections. Configure interval based on NAT/firewall timeouts. Use application-level heartbeat for early detection. Handle: missed heartbeats, half-open connections.

## p10: Rate Limiting
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: networking
category: other
```

- Primitives: RateLimit (requests_per_window, window_size), RateLimitScope (global, per_client, per_endpoint).
- Invariants: Requests exceeding RateLimit MUST be rejected with 429 (networking.inv.9).
- Triggers: rate_limit_exceeded, burst_detected.
- RULE: Implement rate limiting at edge or per-service. Define scope: global, per-client (API key, IP), per-endpoint. Return 429 with Retry-After header. Use token bucket or sliding window. Document limits in API contract.

## p11: Proxy and Gateway Contract
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: networking
category: other
```

- Primitives: Proxy (type: forward, reverse, transparent), Gateway (routes, policies).
- Triggers: proxy_error, route_not_found.
- RULE: Document proxy/gateway in path. Configure: routing rules, header manipulation, authentication, rate limiting. Handle: proxy failures, upstream unavailable. Monitor proxy latency and errors.

## p12: Network Segmentation
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: networking
category: other
```

- Primitives: NetworkZone (trust_level, allowed_flows), FirewallRule, SecurityGroup.
- Invariants: Traffic MUST NOT flow between zones without explicit FirewallRule (networking.inv.10).
- Triggers: unauthorized_flow, segmentation_violation.
- RULE: Define NetworkZones (public, DMZ, private, data). Configure allowed traffic flows. Deny by default. Log and alert on violations. Review rules periodically. Coordinate with security.p1.
