# API Design & Contracts (Compressed)
# ID: api
# Module key (for fragment IDs): `api_design` (see `master_index.yaml.pattern_map`)
# Version: 1.0.0
# Status: active
# Last reviewed: 2026-02-23
# Assumptions: Boundaries governs contracts; schema_evolve governs versioning; this governs API semantics and developer experience.
# License: CC-BY-4.0
# License URL: https://creativecommons.org/licenses/by/4.0/
# Origin: maintainer
# Adoption Status: adopted
# Standard Inclusion: canonical-reference
# Canonical Manifest Pin: FITPAC 1.0.0 reference distribution

## p1: API Style Selection
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: api
category: other
```

- Primitives: APIStyle (REST, GraphQL, gRPC, RPC, AsyncAPI), StyleProfile.
- Invariants: API style MUST be declared and consistently applied (api_design.inv.1).
- Triggers: style_inconsistency, style_mismatch.
- RULE: Select APIStyle based on: client diversity (REST: universal), query flexibility (GraphQL), performance (gRPC), event-driven (AsyncAPI). Document selection rationale. Mix allowed at different layers but not within single API.

## p2: Resource Modeling
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: api
category: other
```

- Primitives: Resource (name, attributes, relationships), ResourceIdentifier, ResourceCollection.
- Invariants: Resources MUST have stable, unique identifiers (api_design.inv.2).
- Triggers: identifier_collision, model_ambiguity.
- RULE: Model domain entities as Resources. Use nouns, not verbs (users, orders, not getUser). Define relationships (1:1, 1:N, N:N). Identifiers: opaque, stable, URL-safe. Collections: plural form. Coordinate with ontology.p1.

## p3: HTTP Semantics
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: api
category: other
```

- Primitives: HTTPMethod (GET, POST, PUT, PATCH, DELETE), MethodSemantics (safe, idempotent).
- Invariants: Methods MUST adhere to HTTP semantics (api_design.inv.3).
- Triggers: method_misuse, unsafe_get.
- RULE: GET: safe, idempotent, cacheable. POST: create or action, not idempotent. PUT: full replace, idempotent. PATCH: partial update. DELETE: remove, idempotent. No side effects on GET. Coordinate with temporal.p1 for idempotency.

## p4: Status Code Contract
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: api
category: other
```

- Primitives: HTTPStatusCode, StatusCodeMapping.
- Invariants: Status codes MUST accurately reflect operation outcome (api_design.inv.4).
- Triggers: status_code_mismatch.
- RULE: 2xx: success (200 OK, 201 Created, 204 No Content). 4xx: client error (400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, 409 Conflict, 429 Rate Limited). 5xx: server error (500 Internal, 503 Unavailable). Map to boundaries.p2 taxonomy.

## p5: Request/Response Schema
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: api
category: other
```

- Primitives: RequestSchema, ResponseSchema, SchemaValidation.
- Invariants: Requests MUST validate against schema before processing (api_design.inv.5).
- Triggers: schema_violation, invalid_request.
- RULE: Define schemas (JSON Schema, OpenAPI, Protobuf). Validate requests. Reject invalid with 400 and specific errors. Document schemas. Generate schemas from code or vice versa. Test schema validation. Extends security.p4 (IOContract).

## p6: Pagination Contract
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: api
category: other
```

- Primitives: PaginationStyle (offset, cursor, keyset), PageParams (limit, offset/cursor), PageResponse (items, total, next).
- Invariants: Collection endpoints MUST support pagination (api_design.inv.6).
- Triggers: unbounded_response, pagination_drift.
- RULE: Choose PaginationStyle: Offset (simple, fragile on updates), Cursor (stable, opaque), Keyset (performant, requires sort key). Default limit with max cap. Return pagination metadata. Handle: empty pages, concurrent modifications.

## p7: Filtering and Sorting
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: api
category: other
```

- Primitives: FilterExpression, SortExpression, QueryContract.
- Invariants: Filter/sort MUST NOT expose internal fields (api_design.inv.7).
- Triggers: filter_injection, invalid_sort.
- RULE: Define allowed filter fields and operators. Validate filter expressions. Limit complexity to prevent DoS. Define sortable fields. Default sort order. Document query capabilities. Prevent SQL injection via filters.

## p8: Bulk Operations
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: api
category: other
```

- Primitives: BulkRequest (operations), BulkResponse (results, partial_success), BulkLimit.
- Invariants: Bulk operations MUST report per-item results (api_design.inv.8).
- Triggers: bulk_limit_exceeded, partial_failure.
- RULE: Support bulk create/update/delete for efficiency. Define BulkLimit (items per request). Return per-item success/failure. Decide: all-or-nothing vs partial success. Document transaction semantics. Consider async for large batches.

## p9: HATEOAS and Discoverability
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: api
category: other
```

- Primitives: Link (rel, href), HypermediaControl, APIRoot.
- Triggers: broken_link.
- RULE: Include Links for navigation and actions. Standard relations: self, next, prev, related. APIRoot provides entry points. Enables API evolution. Clients follow links rather than construct URLs. Optional for internal APIs, valuable for public.

## p10: API Versioning
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: api
category: other
```

- Primitives: APIVersion, VersioningStrategy (URL, header, query), VersionLifecycle.
- Invariants: Breaking changes MUST increment major version (api_design.inv.9).
- Triggers: breaking_change, version_sunset.
- RULE: Version APIs from start. Strategies: URL path (/v1/), header (Accept-Version), query param. Prefer URL for visibility. Support N-1 version minimum. Document breaking vs non-breaking changes. Sunset old versions with notice. Extends schema_evolve.p1.

## p11: Rate Limiting Contract
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: api
category: other
```

- Primitives: RateLimitPolicy (tier, limits), RateLimitHeader (X-RateLimit-*).
- Invariants: Rate limits MUST be documented and enforced consistently (api_design.inv.10).
- Triggers: rate_limit_exceeded.
- RULE: Define rate limits per tier (free, paid, enterprise). Return headers: limit, remaining, reset. 429 response with Retry-After. Document limits in API spec. Allow burst with token bucket. Extends networking.p10.

## p12: Authentication and Authorization
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: api
category: other
```

- Primitives: AuthMethod (API key, OAuth, JWT, mTLS), AuthScope, AuthError.
- Invariants: Protected endpoints MUST verify authentication before processing (api_design.inv.11).
- Triggers: auth_required, auth_failed, scope_insufficient.
- RULE: Document AuthMethod per endpoint. Validate credentials early. Check scopes/permissions. Return 401 (not authenticated) vs 403 (not authorized). Don't leak existence via auth errors. Coordinate with security.p2.

## p13: Idempotency Contract
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: api
category: other
```

- Primitives: IdempotencyKey (header or param), IdempotencyWindow.
- Invariants: Replayed requests with same IdempotencyKey MUST return original response (api_design.inv.12).
- Triggers: duplicate_request, idempotency_expired.
- RULE: For non-idempotent operations (POST), accept IdempotencyKey. Store request-response mapping. Return stored response for duplicates. Define IdempotencyWindow (e.g., 24 hours). Document idempotency support. Extends temporal.p1.

## p14: Webhook Contract
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: api
category: other
```

- Primitives: WebhookSubscription (url, events, secret), WebhookDelivery (retry_policy, signature).
- Invariants: Webhook payloads MUST be signed for verification (api_design.inv.13).
- Triggers: webhook_failed, signature_invalid.
- RULE: Support webhook subscriptions for async events. Sign payloads with shared secret (HMAC). Retry failed deliveries with backoff. Include event type and timestamp. Document payload schemas. Allow subscription management via API.

## p15: API Documentation
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: api
category: other
```

- Primitives: APISpec (OpenAPI, AsyncAPI, GraphQL SDL), APIDocumentation.
- Invariants: API MUST have machine-readable specification (api_design.inv.14).
- Triggers: spec_outdated, undocumented_endpoint.
- RULE: Generate APISpec from code or maintain manually. Include: endpoints, schemas, examples, auth, errors. Keep spec in sync with implementation. Publish documentation. Enable client generation from spec. Test examples work.
