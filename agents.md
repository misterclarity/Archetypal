# agents.md -- Fleet Manifest

The birth chart of an agent fleet: every agent's identity, role, governance policy, communication topology, and lifecycle schedule in one file. Each section is a template followed by a worked example (the Research Fleet from Chapter 7). Copy the templates, delete the examples, and keep the file current -- an outdated manifest is worse than no manifest at all.

---

## Fleet Identity (The Sun)

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
  version: "2.2.0"
  owner: "research-ops-team"
  repository: "github.com/org/quantum-research-fleet"
  created: "2025-09-15"
  last_audit: "2026-01-10"
```

---

## Agent Registry (The Twelve Archetypes)

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
  model: ""                         # LLM model identifier, e.g. claude-opus-5-5 for slow/deliberate
                                    # roles, claude-haiku-5-5 for fast/classifier roles. Current IDs
                                    # carry no date suffix; pin a dated snapshot only when the Saturn
                                    # audit requires reproducibility.
  tier: ""                          # "fast" (Moon handler) | "slow" (Sun prompt) | "code" (no model)
  effort: ""                        # low | medium | high | xhigh | max -- the depth dial for the
                                    # model's thinking. Both current models default to medium; set it.
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
    # Neptune / DISSOLVE -- Graceful degradation (what the agent does when its contracts are relaxed)
    degraded_mode: ""               # Behavior when operating in degraded state
```

### Example: Research Fleet Agents

<!-- This fleet implements all five archetypes from the research pipeline example in Chapter 7,
     plus the Governor that owns the saturn: block below. -->

#### Agent: Strategist

```yaml
agent:
  name: "research-strategist"
  archetype: "Strategist"
  sign:
    element: "Fire"
    modality: "Mutable"
  description: "Decomposes research goals into sub-queries, sets success criteria, and determines research horizon"
  model: "claude-opus-5-5"
  tier: "slow"
  effort: "high"
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
  model: "claude-haiku-5-5"
  tier: "fast"
  effort: "low"
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
  model: "claude-opus-5-5"
  tier: "slow"
  effort: "medium"
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
    downstream: ["research-synthesizer"]
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
    fallback_agent: "research-synthesizer"
    circuit_breaker:
      failure_threshold: 2
      recovery_timeout_seconds: 120
    degraded_mode: "pass results with unvalidated flag, alert governor"
```

#### Agent: Synthesizer

```yaml
agent:
  name: "research-synthesizer"
  archetype: "Synthesizer"
  sign:
    element: "Water"
    modality: "Mutable"
  description: "Merges validated fragments into a coherent narrative, finds cross-domain patterns, bridges technical and commercial findings with fuzzy semantic matching"
  model: "claude-opus-5-5"
  tier: "slow"
  effort: "high"
  system_prompt: "./prompts/synthesizer.md"
  tools:
    - "semantic_similarity"
    - "cross_domain_pattern_match"
    - "narrative_merge"
  input_schema: "./schemas/validated_results.json"
  output_schema: "./schemas/synthesis.json"

  dependencies:
    upstream: ["research-validator"]
    downstream: ["research-presenter"]
    shared_resources: ["research-knowledge-base"]

  execution:
    trigger: "upstream_complete"
    priority: "normal"
    timeout_seconds: 120
    retry_strategy:
      max_retries: 1
      backoff: "none"
      retry_on: ["timeout"]

  fallback:
    fallback_agent: "research-presenter"
    circuit_breaker:
      failure_threshold: 3
      recovery_timeout_seconds: 180
    degraded_mode: "pass validated fragments through unsynthesized, with gaps flagged 'no narrative'"
```

#### Agent: Presenter

```yaml
agent:
  name: "research-presenter"
  archetype: "Presenter"
  sign:
    element: "Fire"
    modality: "Fixed"
  description: "Formats the synthesized narrative into executive summary, key findings, visual charts, and recommended actions"
  model: "claude-opus-5-5"
  tier: "slow"
  effort: "low"
  system_prompt: "./prompts/presenter.md"
  tools:
    - "markdown_formatter"
    - "chart_generator"
    - "executive_summary_template"
  input_schema: "./schemas/synthesis.json"
  output_schema: "./schemas/briefing_document.json"

  dependencies:
    upstream: ["research-synthesizer"]
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
    degraded_mode: "output the synthesized narrative as plaintext"
```

#### Agent: Governor

```yaml
agent:
  name: "research-governor"
  archetype: "Governor"
  sign:
    element: "Earth"
    modality: "Cardinal"
  description: "Owns the saturn: block. The LIMIT gate itself is deterministic code; this agent reviews escalations, budget freezes and audit findings, and is the only agent allowed to change thresholds"
  model: "claude-opus-5-5"            # used for review only; the gate never calls a model
  tier: "code"
  effort: "high"
  system_prompt: "./prompts/governor.md"
  tools:
    - "policy_engine"
    - "budget_ledger"
    - "threshold_registry"
  input_schema: "./schemas/messages/envelope.json"
  output_schema: "./schemas/governor_ruling.json"

  dependencies:
    upstream: ["*"]
    downstream: []
    shared_resources: ["budget_ledger"]

  execution:
    trigger: "event"
    priority: "critical"
    timeout_seconds: 300
    retry_strategy:
      max_retries: 0
      backoff: "none"
      retry_on: []

  fallback:
    fallback_agent: null
    circuit_breaker:
      failure_threshold: 1
      recovery_timeout_seconds: 0
    degraded_mode: "fail closed: freeze the escalating agent until a human rules"
```

---

## Governance Layer (Planetary Operators)

### Saturn / LIMIT -- Guardrails & Policy Enforcement

```yaml
saturn:
  rate_limits:
    requests_per_minute_per_agent: 0      # Max requests any single agent can make
    requests_per_minute_fleet_wide: 0     # Max requests across the entire fleet
    concurrent_agents_max: 0              # Max agents executing simultaneously
    max_tokens_per_task: 0                # Token ceiling per task, across both threads
    max_tool_calls_per_task: 0            # Tool-call ceiling per task

  cost_caps:
    max_cost_per_task_usd: 0.00           # Hard ceiling per individual task (keep >= 2x one slow call)
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

  forbidden_actions: []                   # Actions no agent may ever take, at any confidence
```

#### Example: Research Fleet Saturn

```yaml
saturn:
  rate_limits:
    requests_per_minute_per_agent: 30
    requests_per_minute_fleet_wide: 100
    concurrent_agents_max: 4
    max_tokens_per_task: 24000
    max_tool_calls_per_task: 8

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
  schema_registry: ""                     # Path to message schema definitions; the envelope every hop
                                          # shares lives here (e.g. ./schemas/messages/envelope.json)
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
  roadmap: []                             # North Node / IMPORT: capabilities the fleet needs but has not loaded
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
  roadmap:
    - "accumulator agent to own research-knowledge-base"
    - "auditor job to purge stale credibility scores"
```

### Pluto / REFORMAT -- Retirement & Migration Policy

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
  deprecation_backlog: []                 # South Node / ARCHIVE: cached defaults the fleet runs on autopilot
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
  deprecation_backlog:
    - "legacy search endpoint (returns 200 with 72h-stale data)"
```

---

## Cognition Layer (The Moon / The Sun -- Fast and Slow Threads)

The two-speed brain from Chapter 7. The fast thread classifies every input; the slow thread deliberates when the fast thread may not act alone; Saturn owns the thresholds; the learning loop turns slow decisions into fast examples. The keys mirror `brain/archetypal_brain.py` so the manifest and the code agree.

```yaml
brain:
  fast_thread:                            # Moon / BUFFER
    model: "claude-haiku-5-5"
    effort: "low"
    labels: ["Initiator", "Accumulator", "Router", "Guardian", "Presenter", "Validator",
             "Mediator", "Auditor", "Strategist", "Governor", "Innovator", "Synthesizer"]
    output_schema: "./schemas/moon_verdict.json"       # {sign, confidence, risk, rationale}
    handler_registry: "./handlers/"
    examples_per_call: 6                  # nearest Sun-labeled precedents pasted in as few-shot
    max_latency_ms: 800
    cache_system_prompt: true             # explicit breakpoint on the system block; engages only above the
                                          # model's minimum cacheable prefix (check usage.cache_read_input_tokens)

  slow_thread:                            # Sun / IDENTITY
    model: "claude-opus-5-5"
    effort_deliberate: "high"
    effort_verify: "low"
    output_schema: "./schemas/decision.json"           # {sign, action, response, risk, confidence, rationale, needs_human, rule}
    max_latency_ms: 60000
    complement_review: true               # the opposite archetype reviews before the handler runs

  thresholds:                             # Saturn owns these; the Auditor only tightens them
    reflex_confidence: 0.85               # Moon acts alone at or above this
    verify_confidence: 0.70               # between verify and reflex: Sun checks the Moon's draft at low effort
    reflex_max_novelty: 0.60              # 1.0 = nothing similar in memory
    slow_only: ["Initiator", "Auditor", "Governor", "Innovator", "Strategist"]
    risk_floor:                           # the Moon may raise a risk grade, never lower it below these
      Initiator: "medium"
      Auditor: "medium"
      Governor: "medium"
      Innovator: "medium"

  hard_escalation:
    on_forbidden_action: "hold_for_human"
    on_irreversible_side_effect: "deliberate"
    on_pii: "redact_before_anything_else"
    on_budget_exhausted: "hold_for_human"        # a Sun that cannot run is never scored as a disagreement
    on_api_error: "degrade"                      # Moon -> untrusted verdict; Sun -> hold; reviewer -> reject
    on_complement_rejects_reflex: "interrupt"   # Uranus: one re-run on the slow thread

  learning_loop:                          # South Node / ARCHIVE and North Node / IMPORT
    decision_log: "./memory.jsonl"        # Taurus store; redacted text only (mock runs use memory.mock.jsonl)
    examples_from: ["slow", "verify"]     # reflex-only records are never training examples
    shadow_every: 10                      # Scorpio: every Nth reflex re-judged by the Sun at low effort
    shadow_window: 10                     # the tighten rule's evidence window; stale disagreements expire
    tighten_rule: "shadow-check disagreement > 0.20 over the last shadow_window shadow checks -> reflex_confidence += 0.02, one step per window, persisted in memory.policy.json"
    loosen_rule: "never automatic; human sign-off in a maintenance window"
    pluto_rebuild: "keep the last 500 Sun-labeled records; drop reflex-only records"
    import_signal: "inputs with novelty > 0.8 counted at the Jupiter review -> candidate new handler"
```

---

## Agent Pairings (The Six Axes)

| Axis | Agent A | Agent B | Balance Function |
|------|---------|---------|------------------|
| Identity (Aries-Libra) | Initiator | Mediator | Action is checked by impact assessment |
| Substance (Taurus-Scorpio) | Accumulator | Auditor | Persistence is checked by garbage collection |
| Mind (Gemini-Sagittarius) | Router | Strategist | Data collection is checked by synthesis |
| Foundation (Cancer-Capricorn) | Guardian | Governor | Privacy is checked by policy enforcement |
| Expression (Leo-Aquarius) | Presenter | Innovator | Output stability is checked by experimentation |
| Service (Virgo-Pisces) | Validator | Synthesizer | Strict verification is checked by fuzzy integration |

### Fleet Balance Audit

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
    synthesizer_present: true             # research-synthesizer
  foundation:
    guardian_present: false               # ACCEPTABLE: public research sources, no PII in the pipeline
    governor_present: true                # research-governor
  expression:
    presenter_present: true               # research-presenter
    innovator_present: false              # ACCEPTABLE: Fleet does not require experimentation axis
  substance:
    accumulator_present: false            # WARNING: research-knowledge-base and credibility-database
    auditor_present: false                #   are persisted by nobody and purged by nobody.
    # Recommendation: give the knowledge base an Accumulator owner and a nightly Auditor purge
    # (both are on the Jupiter roadmap above)
```

---

## Communication Topology (Aspects)

<!-- Classify every hand-off by the real angle between the two agents' signs (Chapter 4):
     same element = trine, compatible element = sextile, same modality = square or opposition,
     nothing shared = quincunx. Document every square. Define the resource contract. Decide who wins. -->

### Conjunctions (Tightly Coupled Agents)

```yaml
conjunctions: []
  # - agents: ["agent_a", "agent_b"]
  #   shared_resource: ""
  #   risk: "High coupling -- changes to one affect the other"
  #   mitigation: ""
```

### Oppositions (Distributed Pairs)

```yaml
oppositions: []
  # - agents: ["agent_a", "agent_b"]
  #   communication_channel: ""
  #   latency_budget_ms: 0
  #   risk: "Network partition can break communication"
  #   mitigation: ""
```

### Squares (Known Contention Points)

```yaml
squares: []
  # - agents: ["agent_a", "agent_b"]
  #   contested_resource: ""
  #   conflict_resolution: ""          # "agent_a_wins" | "agent_b_wins" | "queue" | "arbiter"
  #   risk: "Deadlock or resource starvation"
  #   mitigation: ""
```

### Trines (Optimized Pipelines)

```yaml
trines: []
  # - agents: ["agent_a", "agent_b"]
  #   data_flow: "a -> b"
  #   format_compatibility: "native"   # a's output_schema IS b's input_schema, no adapter
  #   throughput_target: ""
```

### Quincunxes (Adapter Required)

```yaml
quincunxes: []
  # - agents: ["agent_a", "agent_b"]
  #   adapter: ""                      # Path to the translation layer
  #   risk: "No shared format -- silent drift between the two sides"
  #   mitigation: ""
```

#### Example: Research Fleet Topology

```yaml
trines:
  - agents: ["research-strategist", "research-presenter"]    # Fire -> Fire (Sagittarius -> Leo, 120°)
    data_flow: "strategist -> presenter"
    format_compatibility: "native (research_plan.json sections become the briefing skeleton)"
    throughput_target: "< 3s handoff"

oppositions:
  - agents: ["research-strategist", "research-router"]       # Mind axis: Sagittarius <-> Gemini, 180°
    communication_channel: "redis queue: research_plans"
    latency_budget_ms: 5000
    risk: "Router starts fetching before the plan is final"
    mitigation: "plans are versioned; router consumes only plans marked final"
  - agents: ["research-validator", "research-synthesizer"]   # Service axis: Virgo <-> Pisces, 180°
    communication_channel: "redis queue: validated_results"
    latency_budget_ms: 10000
    risk: "Synthesizer merges fragments the validator later rejects"
    mitigation: "synthesizer consumes only results with validation_status: passed"

squares:
  - agents: ["research-router", "research-validator"]        # both Mutable: Gemini -> Virgo, 90°
    contested_resource: "raw_results throughput (router floods, validator gates)"
    conflict_resolution: "agent_b_wins"                      # the validator sets the acceptance rate
    risk: "Validator backlog starves the pipeline"
    mitigation: "router honours validator backpressure; queue depth triggers jupiter scale-up"
  - agents: ["jupiter.auto_scale", "saturn.rate_limits"]     # Jupiter/Saturn: MULTIPLY against LIMIT -- same resolution as Chapter 7's Mars/Saturn square
    contested_resource: "concurrent_agents_max (4) vs max_instances_per_agent (3) x 6 agents = 18"
    conflict_resolution: "agent_b_wins"                      # Saturn sets the ceiling; Jupiter scales within it
    risk: "scale-up events that can never be honoured; queue_depth trigger fires forever"
    mitigation: "auto_scale reads concurrent_agents_max as its hard cap; alert when cap-bound > 15 min"

quincunxes:
  - agents: ["research-synthesizer", "research-presenter"]   # Pisces -> Leo, 150°: no shared element or modality
    adapter: "./adapters/synthesis_to_briefing.py"
    risk: "Narrative prose does not map cleanly onto rich sections"
    mitigation: "synthesizer emits section anchors the presenter keys on"
```

---

## Lifecycle Schedule (Transits)

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
    - "Review the brain's handler-usage histogram and high-novelty inputs (North Node)"
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
    - "Re-run shadow evaluation: Moon vs Sun agreement per label; tighten any label below 0.85"
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
    - "A reflex label's Moon-vs-Sun agreement collapses (re-baseline thresholds after any model swap)"
  migration_playbook: ""                  # Path to migration procedure
  rollback_playbook: ""                   # Path to rollback procedure
  estimated_downtime: ""
```

### Pluto Trigger -- Full Replatforming

```yaml
pluto_trigger:
  trigger_conditions:
    - "Entire model family replaced (e.g., one generation of models -> the next)"
    - "Infrastructure provider migration (e.g., AWS -> GCP)"
    - "Fundamental architectural redesign required"
    - "Fleet purpose has changed beyond original design parameters"
  replatform_playbook: ""                 # Path to replatforming procedure
  data_preservation_plan: ""              # How historical data and state are preserved
  parallel_run_duration: ""               # How long old and new fleets run simultaneously
```

---

## Monitoring & Observability (The Moon / BUFFER)

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
      # the brain's own metrics
      - "reflex_hit_rate"               # fast decisions / all decisions
      - "moon_sun_disagreement"         # per label, from verify + shadow comparisons
      - "escalation_rate"               # decisions held for a human / all decisions
      - "interrupt_rate"                # reflexes overruled by the complement review
      - "novelty_p95"                   # rising = the world changed, the cache is stale
      - "cost_per_decision_usd"
      - "p95_latency_fast_ms"
      - "p95_latency_slow_ms"
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
      - name: "reflex_rot"
        condition: "moon_sun_disagreement > 0.20 over last 100 comparisons for any label"
        severity: "warning"
        action: "notify -- tighten reflex_confidence; move the label to slow_only until the Saturn audit"
      - name: "novelty_surge"
        condition: "novelty_p95 up 50% week over week"
        severity: "warning"
        action: "notify -- North Node candidate; review at the Jupiter cycle"
      - name: "fast_path_collapse"
        condition: "reflex_hit_rate < 0.50 for 24h"
        severity: "info"
        action: "notify -- cost review"

  metrics:
    collection_interval_seconds: 60
    key_metrics:
      - "task_completion_rate"
      - "average_latency_ms"
      - "cost_per_task_usd"
      - "error_rate_percent"
      - "token_usage_per_agent"
      - "queue_depth"
      - "reflex_hit_rate"
      - "moon_sun_disagreement"
      - "escalation_rate"
      - "interrupt_rate"
      - "novelty_p95"
      - "cost_per_decision_usd"
```

---

## Security (Cancer / Guardian Configuration)

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
    redact_before_model_or_memory: true   # the brain's Guardian step: models and the decision log see redacted text only

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
      research-synthesizer:
        - "read:validated_results"
        - "write:synthesis"
      research-presenter:
        - "read:synthesis"
        - "read:output_templates"
        - "write:briefing_documents"
      research-governor:
        - "read:*"
        - "write:thresholds"
        - "write:budget_ledger"

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
    redact_before_model_or_memory: true

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

<!-- Ruling Operator = the sign's ruling planet (Chapter 6, chart rulers; Chapter 7, "Each Archetype Has a Native Operator") -->

| If your agent needs to... | Use Archetype | Sign | Ruling Operator |
|---|---|---|---|
| Start new tasks fast with no dependencies | **Initiator** | Aries | `VECTOR` |
| Maintain long-running state reliably | **Accumulator** | Taurus | `BIND` |
| Route messages across multiple channels | **Router** | Gemini | `IO_STREAM` |
| Protect sensitive data and control access | **Guardian** | Cancer | `BUFFER` |
| Produce polished user-facing output | **Presenter** | Leo | `IDENTITY` |
| Validate outputs against strict schemas | **Validator** | Virgo | `IO_STREAM` |
| Orchestrate multi-agent consensus | **Mediator** | Libra | `BIND` |
| Detect anomalies and audit behavior | **Auditor** | Scorpio | `REFORMAT` |
| Decompose goals and plan strategy | **Strategist** | Sagittarius | `MULTIPLY` |
| Enforce policy, budgets, and compliance | **Governor** | Capricorn | `LIMIT` |
| Experiment with novel approaches | **Innovator** | Aquarius | `INTERRUPT` |
| Synthesize across disparate sources | **Synthesizer** | Pisces | `DISSOLVE` |

---
