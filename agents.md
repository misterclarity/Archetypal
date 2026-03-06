# agents.md -- Fleet Manifest

<!-- This is the birth chart of your agent system. -->
<!-- Every section maps to a component of the Archetypal Operating System. -->
<!-- Copy this file. Customize every field. Keep it updated. -->
<!-- An outdated manifest is worse than no manifest at all. -->

---

## Fleet Identity (The Sun)

<!-- The Sun is the IDENTITY operator. Without it, you have a process without a PID. -->

```yaml
fleet:
  name: ""                          # The fleet's declared identity
  purpose: ""                       # One sentence: why does this fleet exist?
  version: "1.0.0"                  # Semantic versioning of the fleet architecture
  owner: ""                         # Team or individual responsible
  repository: ""                    # Source of truth for fleet configuration
  created: ""                       # ISO 8601 date of initial deployment
  last_audit: ""                    # ISO 8601 date of last Saturn cycle audit
```

### Example: Research Fleet

```yaml
fleet:
  name: "quantum-research-fleet"
  purpose: "Autonomously research, validate, and synthesize briefing documents on emerging technology topics"
  version: "2.1.0"
  owner: "research-ops-team"
  repository: "github.com/org/quantum-research-fleet"
  created: "2025-09-15"
  last_audit: "2026-01-10"
```

---

## Agent Registry (The Twelve Archetypes)

<!-- Each agent occupies a sign-based archetype. -->
<!-- The archetype determines the agent's fundamental execution profile. -->
<!-- You do not need all twelve. You need the ones your fleet requires. -->
<!-- But remember the Axes: never deploy one pole without its complement. -->

### Agent Template

```yaml
agent:
  name: ""                          # Unique identifier (Sun/IDENTITY)
  archetype: ""                     # One of: Initiator, Accumulator, Router, Guardian,
                                    #         Presenter, Validator, Mediator, Auditor,
                                    #         Strategist, Governor, Innovator, Synthesizer
  sign:
    element: ""                     # Fire, Earth, Air, or Water
    modality: ""                    # Cardinal (init), Fixed (persist), Mutable (transform)
  description: ""                   # What this agent does in plain language
  model: ""                         # LLM model identifier (e.g., claude-sonnet-4-6)
  system_prompt: ""                 # Path to system prompt file or inline prompt
  tools: []                         # List of tools/APIs this agent can access
  input_schema: ""                  # Expected input format (JSON schema path or inline)
  output_schema: ""                 # Expected output format (JSON schema path or inline)

  # Venus / BIND -- Dependencies
  dependencies:
    upstream: []                    # Agents that feed into this agent
    downstream: []                  # Agents this agent feeds into
    shared_resources: []            # Resources this agent shares with others

  # Mars / VECTOR -- Execution Policy
  execution:
    trigger: ""                     # "event" | "schedule" | "manual" | "upstream_complete"
    priority: ""                    # "critical" | "high" | "normal" | "low"
    timeout_seconds: 0              # Maximum execution time before forced termination
    retry_strategy:
      max_retries: 0
      backoff: ""                   # "linear" | "exponential" | "none"
      retry_on: []                  # Error codes that trigger retry

  # Uranus / INTERRUPT -- Fallback
  fallback:
    fallback_agent: ""              # Agent to invoke if this agent fails
    circuit_breaker:
      failure_threshold: 0          # Number of failures before circuit opens
      recovery_timeout_seconds: 0   # Time before circuit half-opens
    degraded_mode: ""               # Behavior when operating in degraded state
```

### Example: Research Fleet Agents

<!-- This fleet uses 4 archetypes from the research pipeline example in Chapter 7. -->

#### Agent: Strategist

```yaml
agent:
  name: "research-strategist"
  archetype: "Strategist"
  sign:
    element: "Fire"
    modality: "Mutable"
  description: "Decomposes research goals into sub-queries, sets success criteria, and determines research horizon"
  model: "claude-sonnet-4-6"
  system_prompt: "./prompts/strategist.md"
  tools:
    - "goal_decomposition"
    - "criteria_definition"
    - "timeline_estimation"
  input_schema: "./schemas/research_goal.json"
  output_schema: "./schemas/research_plan.json"

  dependencies:
    upstream: []
    downstream: ["research-router"]
    shared_resources: ["research-knowledge-base"]

  execution:
    trigger: "manual"
    priority: "high"
    timeout_seconds: 120
    retry_strategy:
      max_retries: 2
      backoff: "exponential"
      retry_on: ["timeout", "rate_limit"]

  fallback:
    fallback_agent: "research-router"
    circuit_breaker:
      failure_threshold: 3
      recovery_timeout_seconds: 300
    degraded_mode: "pass goal directly to router without decomposition"
```

#### Agent: Router

```yaml
agent:
  name: "research-router"
  archetype: "Router"
  sign:
    element: "Air"
    modality: "Mutable"
  description: "Dispatches sub-queries across multiple data sources in parallel, manages channel multiplexing and deduplication"
  model: "claude-haiku-4-5-20251001"
  system_prompt: "./prompts/router.md"
  tools:
    - "arxiv_search"
    - "news_api"
    - "patent_database"
    - "web_search"
    - "semantic_scholar"
  input_schema: "./schemas/research_plan.json"
  output_schema: "./schemas/raw_results.json"

  dependencies:
    upstream: ["research-strategist"]
    downstream: ["research-validator"]
    shared_resources: ["api-rate-pool"]

  execution:
    trigger: "upstream_complete"
    priority: "normal"
    timeout_seconds: 180
    retry_strategy:
      max_retries: 3
      backoff: "linear"
      retry_on: ["timeout", "rate_limit", "source_unavailable"]

  fallback:
    fallback_agent: null
    circuit_breaker:
      failure_threshold: 5
      recovery_timeout_seconds: 600
    degraded_mode: "reduce to available sources only, flag incomplete coverage"
```

#### Agent: Validator

```yaml
agent:
  name: "research-validator"
  archetype: "Validator"
  sign:
    element: "Earth"
    modality: "Mutable"
  description: "Checks source credibility, cross-references claims, flags contradictions, enforces citation schema"
  model: "claude-sonnet-4-6"
  system_prompt: "./prompts/validator.md"
  tools:
    - "citation_checker"
    - "credibility_scorer"
    - "contradiction_detector"
    - "schema_enforcer"
  input_schema: "./schemas/raw_results.json"
  output_schema: "./schemas/validated_results.json"

  dependencies:
    upstream: ["research-router"]
    downstream: ["research-presenter"]
    shared_resources: ["credibility-database"]

  execution:
    trigger: "upstream_complete"
    priority: "high"
    timeout_seconds: 90
    retry_strategy:
      max_retries: 1
      backoff: "none"
      retry_on: ["timeout"]

  fallback:
    fallback_agent: "research-presenter"
    circuit_breaker:
      failure_threshold: 2
      recovery_timeout_seconds: 120
    degraded_mode: "pass results with unvalidated flag, alert governor"
```

#### Agent: Presenter

```yaml
agent:
  name: "research-presenter"
  archetype: "Presenter"
  sign:
    element: "Fire"
    modality: "Fixed"
  description: "Formats validated research into executive summary, key findings, visual charts, and recommended actions"
  model: "claude-sonnet-4-6"
  system_prompt: "./prompts/presenter.md"
  tools:
    - "markdown_formatter"
    - "chart_generator"
    - "executive_summary_template"
  input_schema: "./schemas/validated_results.json"
  output_schema: "./schemas/briefing_document.json"

  dependencies:
    upstream: ["research-validator"]
    downstream: []
    shared_resources: ["output-templates"]

  execution:
    trigger: "upstream_complete"
    priority: "normal"
    timeout_seconds: 60
    retry_strategy:
      max_retries: 2
      backoff: "linear"
      retry_on: ["timeout", "format_error"]

  fallback:
    fallback_agent: null
    circuit_breaker:
      failure_threshold: 3
      recovery_timeout_seconds: 180
    degraded_mode: "output raw validated results as plaintext"
```

---

## Governance Layer (Planetary Operators)

<!-- These are the management functions that keep the fleet bounded, aligned, and alive. -->
<!-- Saturn is the most critical. Deploy it first. -->

### Saturn / LIMIT -- Guardrails & Policy Enforcement

<!-- Saturn says: define your limits before you deploy. -->

```yaml
saturn:
  rate_limits:
    requests_per_minute_per_agent: 0      # Max requests any single agent can make
    requests_per_minute_fleet_wide: 0     # Max requests across the entire fleet
    concurrent_agents_max: 0              # Max agents executing simultaneously

  cost_caps:
    max_cost_per_task_usd: 0.00           # Hard ceiling per individual task
    max_cost_per_hour_usd: 0.00           # Hard ceiling per hour
    max_cost_per_day_usd: 0.00            # Hard ceiling per day
    alert_threshold_percent: 0            # Alert when this % of budget consumed

  content_filters:
    prohibited_topics: []                 # Topics agents must never generate
    required_disclaimers: []              # Disclaimers that must appear in output
    pii_detection: ""                     # "block" | "redact" | "flag" | "none"
    output_max_length_tokens: 0           # Maximum output length per response

  escalation_policy:
    on_budget_exceeded: ""                # "freeze_agent" | "notify_governor" | "degrade"
    on_content_violation: ""              # "block_output" | "flag_and_release" | "alert"
    on_repeated_failure: ""               # "circuit_break" | "swap_fallback" | "alert"
    escalation_channel: ""                # Where alerts go (email, slack channel, webhook)

  forbidden_actions: []                   # Actions no agent may ever take
```

#### Example: Research Fleet Saturn

```yaml
saturn:
  rate_limits:
    requests_per_minute_per_agent: 30
    requests_per_minute_fleet_wide: 100
    concurrent_agents_max: 4

  cost_caps:
    max_cost_per_task_usd: 2.50
    max_cost_per_hour_usd: 15.00
    max_cost_per_day_usd: 100.00
    alert_threshold_percent: 80

  content_filters:
    prohibited_topics: ["weapons_development", "illegal_activity"]
    required_disclaimers: ["AI-generated research summary"]
    pii_detection: "redact"
    output_max_length_tokens: 8000

  escalation_policy:
    on_budget_exceeded: "freeze_agent"
    on_content_violation: "block_output"
    on_repeated_failure: "circuit_break"
    escalation_channel: "slack:#research-fleet-alerts"

  forbidden_actions:
    - "database_write_without_approval"
    - "external_email_send"
    - "model_self_modification"
```

### Mercury / IO_STREAM -- Messaging Protocol

<!-- Mercury defines how agents speak to each other. No private languages. -->

```yaml
mercury:
  message_format: ""                      # "json" | "protobuf" | "plaintext"
  serialization: ""                       # "json" | "msgpack" | "avro"
  routing_strategy: ""                    # "direct" | "pub_sub" | "broadcast" | "round_robin"
  message_queue: ""                       # Queue service (e.g., "redis", "rabbitmq", "sqs")
  dead_letter_queue: ""                   # Where undeliverable messages go
  retry_on_delivery_failure: false
  max_delivery_retries: 0
  message_ttl_seconds: 0                  # Messages expire after this duration
  schema_validation: false                # Enforce schema on every message
  schema_registry: ""                     # Path to message schema definitions
```

#### Example: Research Fleet Mercury

```yaml
mercury:
  message_format: "json"
  serialization: "json"
  routing_strategy: "direct"
  message_queue: "redis"
  dead_letter_queue: "undeliverable_messages"
  retry_on_delivery_failure: true
  max_delivery_retries: 3
  message_ttl_seconds: 3600
  schema_validation: true
  schema_registry: "./schemas/messages/"
```

### Jupiter / MULTIPLY -- Scaling Policy

<!-- Jupiter asks: where should we grow? -->

```yaml
jupiter:
  auto_scale:
    enabled: false
    trigger_metric: ""                    # "queue_depth" | "latency_p95" | "error_rate"
    scale_up_threshold: 0                 # Metric value that triggers scale-up
    scale_down_threshold: 0               # Metric value that triggers scale-down
    max_instances_per_agent: 0            # Maximum replicas of any single agent
    cooldown_seconds: 0                   # Wait time between scaling events
  load_balancing:
    strategy: ""                          # "round_robin" | "least_connections" | "weighted"
```

#### Example: Research Fleet Jupiter

```yaml
jupiter:
  auto_scale:
    enabled: true
    trigger_metric: "queue_depth"
    scale_up_threshold: 10
    scale_down_threshold: 2
    max_instances_per_agent: 3
    cooldown_seconds: 120
  load_balancing:
    strategy: "least_connections"
```

### Pluto / REFORMAT -- Retirement & Migration Policy

<!-- Pluto does not patch. Pluto replaces. -->

```yaml
pluto:
  deprecation:
    notice_period_days: 0                 # How far in advance to announce retirement
    sunset_date: ""                       # ISO 8601 date when old version is terminated
  migration:
    strategy: ""                          # "blue_green" | "canary" | "rolling" | "big_bang"
    canary_percentage: 0                  # % of traffic to route to new version during canary
    rollback_trigger: ""                  # Metric that triggers automatic rollback
    rollback_plan: ""                     # Path to rollback procedure document
  data_migration:
    state_transfer: ""                    # "full_export" | "incremental_sync" | "none"
    validation_after_migration: false
```

#### Example: Research Fleet Pluto

```yaml
pluto:
  deprecation:
    notice_period_days: 14
    sunset_date: ""
  migration:
    strategy: "canary"
    canary_percentage: 10
    rollback_trigger: "error_rate > 5%"
    rollback_plan: "./runbooks/rollback.md"
  data_migration:
    state_transfer: "incremental_sync"
    validation_after_migration: true
```

---

## Agent Pairings (The Six Axes)

<!-- Never deploy one pole without its complement. -->
<!-- An unbalanced fleet develops the systemic equivalent of a personality disorder. -->

| Axis | Agent A | Agent B | Balance Function |
|------|---------|---------|------------------|
| Identity (Aries-Libra) | Initiator | Mediator | Action is checked by impact assessment |
| Substance (Taurus-Scorpio) | Accumulator | Auditor | Persistence is checked by garbage collection |
| Mind (Gemini-Sagittarius) | Router | Strategist | Data collection is checked by synthesis |
| Foundation (Cancer-Capricorn) | Guardian | Governor | Privacy is checked by policy enforcement |
| Expression (Leo-Aquarius) | Presenter | Innovator | Output stability is checked by experimentation |
| Service (Virgo-Pisces) | Validator | Synthesizer | Strict verification is checked by fuzzy integration |

### Fleet Balance Audit

<!-- Run this check quarterly (Jupiter cycle). For each axis your fleet uses, -->
<!-- verify both poles are present. Flag any axis with only one pole active. -->

```yaml
axis_audit:
  identity:
    initiator_present: false              # Do you have an agent that starts tasks autonomously?
    mediator_present: false               # Do you have an agent that checks for side effects?
  substance:
    accumulator_present: false            # Do you have an agent that persists state?
    auditor_present: false                # Do you have an agent that purges stale state?
  mind:
    router_present: false                 # Do you have an agent that collects data?
    strategist_present: false             # Do you have an agent that synthesizes plans?
  foundation:
    guardian_present: false               # Do you have an agent that protects data?
    governor_present: false               # Do you have an agent that enforces policy?
  expression:
    presenter_present: false              # Do you have an agent that renders output?
    innovator_present: false              # Do you have an agent that experiments?
  service:
    validator_present: false              # Do you have an agent that verifies?
    synthesizer_present: false            # Do you have an agent that integrates?
```

#### Example: Research Fleet Axis Audit

```yaml
axis_audit:
  mind:
    router_present: true                  # research-router
    strategist_present: true              # research-strategist
  service:
    validator_present: true               # research-validator
    synthesizer_present: false            # WARNING: No Pisces complement deployed
    # Recommendation: Add a synthesizer agent to prevent validation bottlenecks
  expression:
    presenter_present: true               # research-presenter
    innovator_present: false              # ACCEPTABLE: Fleet does not require experimentation axis
```

---

## Communication Topology (Aspects)

<!-- Map how your agents are wired together. -->
<!-- Conjunctions are fast but fragile. Oppositions are resilient but slow. -->
<!-- Squares are where your incidents will come from. Trines are your happy paths. -->

### Conjunctions (Tightly Coupled Agents)

<!-- These agents share a process or memory space. Change one, you change both. -->

```yaml
conjunctions: []
  # - agents: ["agent_a", "agent_b"]
  #   shared_resource: ""
  #   risk: "High coupling -- changes to one affect the other"
  #   mitigation: ""
```

### Oppositions (Distributed Pairs)

<!-- These agents are fully independent. They communicate only via message queue. -->

```yaml
oppositions: []
  # - agents: ["agent_a", "agent_b"]
  #   communication_channel: ""
  #   latency_budget_ms: 0
  #   risk: "Network partition can break communication"
  #   mitigation: ""
```

### Squares (Known Contention Points)

<!-- These agents compete for the same resource. This is where incidents live. -->
<!-- Document every square. Define the resource contract. Decide who wins conflicts. -->

```yaml
squares: []
  # - agents: ["agent_a", "agent_b"]
  #   contested_resource: ""
  #   conflict_resolution: ""          # "agent_a_wins" | "agent_b_wins" | "queue" | "arbiter"
  #   risk: "Deadlock or resource starvation"
  #   mitigation: ""
```

### Trines (Optimized Pipelines)

<!-- These agents flow naturally into each other. Protect these paths. -->

```yaml
trines:
  # - agents: ["agent_a", "agent_b"]
  #   data_flow: "a -> b"
  #   format_compatibility: "native"
  #   throughput_target: ""
```

#### Example: Research Fleet Topology

```yaml
trines:
  - agents: ["research-strategist", "research-router"]
    data_flow: "strategist -> router"
    format_compatibility: "native (research_plan.json)"
    throughput_target: "< 5s handoff"

  - agents: ["research-router", "research-validator"]
    data_flow: "router -> validator"
    format_compatibility: "native (raw_results.json)"
    throughput_target: "< 10s handoff"

  - agents: ["research-validator", "research-presenter"]
    data_flow: "validator -> presenter"
    format_compatibility: "native (validated_results.json)"
    throughput_target: "< 3s handoff"

squares: []
  # No contention points in this pipeline -- all agents are sequential.
  # If a parallel validation agent is added, document the square here.
```

---

## Lifecycle Schedule (Transits)

<!-- These are mandatory. Skip them and your fleet degrades silently. -->

### Jupiter Cycle -- Quarterly Scaling Review

```yaml
jupiter_cycle:
  frequency: "quarterly"
  next_review: ""                         # ISO 8601 date
  checklist:
    - "Review agent utilization metrics"
    - "Identify underused agents for decommission"
    - "Identify overloaded agents for scaling"
    - "Evaluate new tool integrations"
    - "Run axis balance audit"
    - "Update fleet version if capabilities changed"
  owner: ""
```

### Saturn Cycle -- Annual Architecture Audit

```yaml
saturn_cycle:
  frequency: "annual"
  next_audit: ""                          # ISO 8601 date
  checklist:
    - "Stress test all Saturn guardrails (cost caps, rate limits, content filters)"
    - "Verify all API endpoints are active and returning fresh data"
    - "Audit all system prompts for drift and contradictions"
    - "Confirm all fallback paths and circuit breakers are functional"
    - "Review and renew all authentication credentials"
    - "Validate that escalation channels are monitored"
    - "Run full integration test across entire pipeline"
    - "Document all findings and remediation actions"
  owner: ""
  last_audit_report: ""                   # Path to previous audit report
```

### Uranus Trigger -- Major Version Migration

```yaml
uranus_trigger:
  trigger_conditions:
    - "New model version released with breaking API changes"
    - "Regulatory requirement mandates architecture change"
    - "Core dependency deprecated with no backward compatibility"
    - "Performance degradation exceeds acceptable threshold for 30+ days"
  migration_playbook: ""                  # Path to migration procedure
  rollback_playbook: ""                   # Path to rollback procedure
  estimated_downtime: ""
```

### Pluto Trigger -- Full Replatforming

```yaml
pluto_trigger:
  trigger_conditions:
    - "Entire model family replaced (e.g., GPT-3.5 era -> GPT-4 era -> next gen)"
    - "Infrastructure provider migration (e.g., AWS -> GCP)"
    - "Fundamental architectural redesign required"
    - "Fleet purpose has changed beyond original design parameters"
  replatform_playbook: ""                 # Path to replatforming procedure
  data_preservation_plan: ""              # How historical data and state are preserved
  parallel_run_duration: ""               # How long old and new fleets run simultaneously
```

---

## Monitoring & Observability (The Moon / BUFFER)

<!-- The Moon tracks internal state. Without it, your fleet is amnesiac. -->

```yaml
monitoring:
  state_persistence:
    backend: ""                           # "redis" | "postgres" | "dynamodb" | "filesystem"
    context_window_policy: ""             # "sliding_window" | "summarize_and_truncate" | "full_history"
    max_context_tokens: 0                 # Maximum context size per agent
    memory_cleanup_schedule: ""           # Cron expression for state garbage collection

  logging:
    level: ""                             # "debug" | "info" | "warn" | "error"
    format: ""                            # "json" | "plaintext"
    destination: ""                       # Log aggregation service or file path
    retention_days: 0                     # How long logs are retained
    include_agent_reasoning: false        # Whether to log chain-of-thought

  alerting:
    channels: []                          # Where alerts are sent
    alert_rules:
      - name: ""
        condition: ""                     # e.g., "error_rate > 5% for 5 minutes"
        severity: ""                      # "critical" | "warning" | "info"
        action: ""                        # "page" | "notify" | "log"

  metrics:
    collection_interval_seconds: 0
    key_metrics:
      - "task_completion_rate"
      - "average_latency_ms"
      - "cost_per_task_usd"
      - "error_rate_percent"
      - "token_usage_per_agent"
      - "queue_depth"
```

#### Example: Research Fleet Monitoring

```yaml
monitoring:
  state_persistence:
    backend: "redis"
    context_window_policy: "summarize_and_truncate"
    max_context_tokens: 16000
    memory_cleanup_schedule: "0 3 * * *"

  logging:
    level: "info"
    format: "json"
    destination: "datadog"
    retention_days: 90
    include_agent_reasoning: true

  alerting:
    channels: ["slack:#research-fleet-alerts", "pagerduty:research-team"]
    alert_rules:
      - name: "high_error_rate"
        condition: "error_rate > 5% for 5 minutes"
        severity: "critical"
        action: "page"
      - name: "cost_threshold"
        condition: "daily_cost > 80% of saturn.cost_caps.max_cost_per_day_usd"
        severity: "warning"
        action: "notify"
      - name: "stale_data_source"
        condition: "any source last_updated > 24 hours"
        severity: "warning"
        action: "notify"

  metrics:
    collection_interval_seconds: 60
    key_metrics:
      - "task_completion_rate"
      - "average_latency_ms"
      - "cost_per_task_usd"
      - "error_rate_percent"
      - "token_usage_per_agent"
      - "queue_depth"
```

---

## Security (Cancer / Guardian Configuration)

<!-- Cancer protects. The Guardian agent is the first and last line of defense. -->
<!-- Every field here should be filled before the fleet touches production data. -->

```yaml
security:
  authentication:
    method: ""                            # "api_key" | "oauth2" | "mtls" | "jwt"
    key_rotation_schedule: ""             # Cron expression or interval
    key_storage: ""                       # "vault" | "env_vars" | "secrets_manager"

  authorization:
    model: ""                             # "rbac" | "abac" | "none"
    agent_permissions: {}                 # Map of agent_name -> list of allowed actions
    # Example:
    # research-router:
    #   - "read:arxiv"
    #   - "read:news_api"
    #   - "read:patent_db"
    # research-presenter:
    #   - "write:output_bucket"
    #   - "read:templates"

  data_classification:
    levels: []                            # e.g., ["public", "internal", "confidential", "restricted"]
    default_level: ""                     # Default classification for new data
    handling_rules: {}                    # Map of level -> handling requirements

  pii_handling:
    detection_method: ""                  # "regex" | "ml_classifier" | "hybrid"
    on_detection: ""                      # "block" | "redact" | "encrypt" | "flag"
    redaction_pattern: ""                 # e.g., "[REDACTED]" or "***"
    audit_pii_access: false               # Whether to log all PII access events

  audit_trail:
    enabled: false
    storage: ""                           # Where audit logs are stored
    retention_days: 0
    immutable: false                      # Whether audit logs can be modified
    events_to_audit:
      - "agent_registration"
      - "tool_invocation"
      - "data_access"
      - "policy_violation"
      - "escalation"
      - "agent_retirement"
```

#### Example: Research Fleet Security

```yaml
security:
  authentication:
    method: "api_key"
    key_rotation_schedule: "0 0 1 * *"
    key_storage: "secrets_manager"

  authorization:
    model: "rbac"
    agent_permissions:
      research-strategist:
        - "read:knowledge_base"
        - "write:research_plans"
      research-router:
        - "read:arxiv"
        - "read:news_api"
        - "read:patent_db"
        - "read:web_search"
        - "read:semantic_scholar"
      research-validator:
        - "read:credibility_database"
        - "read:raw_results"
        - "write:validated_results"
      research-presenter:
        - "read:validated_results"
        - "read:output_templates"
        - "write:briefing_documents"

  data_classification:
    levels: ["public", "internal", "confidential"]
    default_level: "internal"
    handling_rules:
      public: "no restrictions"
      internal: "encrypt at rest, no external sharing"
      confidential: "encrypt at rest and in transit, access logging required"

  pii_handling:
    detection_method: "hybrid"
    on_detection: "redact"
    redaction_pattern: "[REDACTED]"
    audit_pii_access: true

  audit_trail:
    enabled: true
    storage: "s3://research-fleet-audit-logs/"
    retention_days: 365
    immutable: true
    events_to_audit:
      - "agent_registration"
      - "tool_invocation"
      - "data_access"
      - "policy_violation"
      - "escalation"
      - "agent_retirement"
```

---

## Quick Reference: Archetype Selection Guide

<!-- Use this table to select the right archetype for your agent's purpose. -->

| If your agent needs to... | Use Archetype | Sign | Operator |
|---|---|---|---|
| Start new tasks fast with no dependencies | **Initiator** | Aries | `VECTOR` |
| Maintain long-running state reliably | **Accumulator** | Taurus | `BIND` |
| Route messages across multiple channels | **Router** | Gemini | `IO_STREAM` |
| Protect sensitive data and control access | **Guardian** | Cancer | `BUFFER` |
| Produce polished user-facing output | **Presenter** | Leo | `IDENTITY` |
| Validate outputs against strict schemas | **Validator** | Virgo | `LIMIT` |
| Orchestrate multi-agent consensus | **Mediator** | Libra | `BIND` |
| Detect anomalies and audit behavior | **Auditor** | Scorpio | `REFORMAT` |
| Decompose goals and plan strategy | **Strategist** | Sagittarius | `MULTIPLY` |
| Enforce policy, budgets, and compliance | **Governor** | Capricorn | `LIMIT` |
| Experiment with novel approaches | **Innovator** | Aquarius | `INTERRUPT` |
| Synthesize across disparate sources | **Synthesizer** | Pisces | `DISSOLVE` |

---

<!-- End of agents.md fleet manifest. -->
<!-- Remember: update this file every time the fleet changes. -->
<!-- An outdated birth chart is a misread system. -->
