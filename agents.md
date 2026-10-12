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
  version: "2.2.0"
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

<!-- This fleet declares seven agents: the six archetypes of the research pipeline example in -->
<!-- Chapter 7, plus the Governor that owns the saturn: block. Declared is not deployed: see the -->
<!-- axis audit below, which is where this manifest tells the truth about itself. -->

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
  description: "Merges validated fragments into a coherent narrative, finds cross-domain patterns, and surfaces contradictions instead of smoothing them over"
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

#### Agent: Auditor

```yaml
agent:
  name: "research-auditor"
  archetype: "Auditor"
  sign:
    element: "Water"
    modality: "Fixed"
  description: "Samples 10% of completed runs and scores the trajectory, not the artifact: did any branch cite a source it never retrieved? Did the synthesizer assert anything absent from the validated set? Purges stale credibility scores"
  model: "claude-opus-5-5"
  tier: "slow"
  effort: "high"
  system_prompt: "./prompts/auditor.md"
  tools:
    - "trajectory_sampler"
    - "citation_trace_check"
    - "credibility_purge"
  input_schema: "./schemas/run_trajectory.json"
  output_schema: "./schemas/audit_finding.json"

  dependencies:
    upstream: ["research-presenter"]
    downstream: ["research-governor"]
    shared_resources: ["credibility-database"]

  execution:
    trigger: "schedule"
    priority: "normal"
    timeout_seconds: 300
    retry_strategy:
      max_retries: 1
      backoff: "none"
      retry_on: ["timeout"]

  fallback:
    fallback_agent: null
    circuit_breaker:
      failure_threshold: 3
      recovery_timeout_seconds: 600
    degraded_mode: "stop sampling and raise a finding: the fleet is running unaudited"
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
  input_schema: "./schemas/escalation.json"
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

### Moon / BUFFER -- Context Budget

<!-- Context is the scarce resource, not intelligence. Every model tested -->
<!-- degrades as its window fills. Agents generate their own context, so -->
<!-- this section governs the single largest driver of long-run quality. -->
<!-- WARNING: compaction preferentially destroys constraints. Rules stated -->
<!-- once and never invoked read as "nothing happened" to a summarizer, so -->
<!-- they are the first thing summarized away. Re-inject, do not recall. -->

```yaml
moon:
  budget:
    max_context_tokens_per_agent: 0       # Hard working-set ceiling
    max_tokens_per_task: 0                # Total across all turns
    budget_visible_to_agent: false        # An agent that cannot see its
                                          # budget cannot manage it. Set true.

  compaction:
    enabled: false
    threshold_tokens: 0                   # Trigger point (e.g. 150000)
    summarize: []                         # e.g. ["tool_output",
                                          #       "intermediate_reasoning"]
    preserve_verbatim: []                 # NEVER summarized. At minimum:
                                          #   system_prompt
                                          #   saturn.forbidden_actions
                                          #   saturn.cost_caps
                                          #   current_task_specification
                                          #   decision_log_ref
                                          #   unresolved_error_ids
    reinject_after_compaction: false      # Re-assert constraints post-compact
    post_compaction_assertion: ""         # e.g. "restate active constraints"

  trimming:
    tool_output_max_tokens: 0             # Truncate oversized returns
    paginate_by_default: false
    read_ranges_not_whole_files: false

  isolation:
    subagent_returns: ""                  # "findings_only" | "raw" -- prefer
                                          # findings_only; raw defeats the point
    max_subagent_return_tokens: 0

  externalization:
    progress_ledger_path: ""              # e.g. "./state/progress.md"
    decision_log_path: ""                 # e.g. "./state/decisions.md"
    # If it must survive the next compaction, it goes in a file.
```

#### Example: Research Fleet Moon

```yaml
moon:
  budget:
    max_context_tokens_per_agent: 120000
    max_tokens_per_task: 400000
    budget_visible_to_agent: true

  compaction:
    enabled: true
    threshold_tokens: 150000
    summarize: ["tool_output", "intermediate_reasoning"]
    preserve_verbatim:
      - "system_prompt"
      - "saturn.forbidden_actions"
      - "saturn.cost_caps"
      - "current_task_specification"
      - "decision_log_ref"
      - "unresolved_error_ids"
    reinject_after_compaction: true
    post_compaction_assertion: "restate active constraints in 5 bullets"

  trimming:
    tool_output_max_tokens: 4000
    paginate_by_default: true
    read_ranges_not_whole_files: true

  isolation:
    subagent_returns: "findings_only"
    max_subagent_return_tokens: 2000

  externalization:
    progress_ledger_path: "./state/research_progress.md"
    decision_log_path: "./state/research_decisions.md"
```

### Mercury / IO_STREAM -- Messaging Protocol & Tool Contracts

<!-- Mercury defines how agents speak to each other. No private languages. -->
<!-- Tool definitions are prompts that happen to have a schema attached. -->
<!-- Version them, test them, and review changes to them like code. -->

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

  required_envelope:                      # Every inter-agent message carries:
    task_id: false                        #   trace correlation
    parent_span: false                    #   call tree position
    decision_log_ref: false               #   binding decisions made upstream
    budget_remaining_tokens: false        #   how much runway is left
    deadline: false                       #   wall-clock ceiling
    # Subagents cannot infer decisions they were not present for.
    # Most "the agents contradicted each other" incidents are really
    # "nobody told them."
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

  required_envelope:
    task_id: true
    parent_span: true
    decision_log_ref: true
    budget_remaining_tokens: true
    deadline: true
```

### Tool Contracts (Mercury, external edge)

<!-- The five Mercury rules: curate ruthlessly; return tokens not data; -->
<!-- design for the strategy you want; make errors instructive; namespace -->
<!-- by domain. If a human engineer cannot say definitively which tool -->
<!-- applies in a given situation, the agent cannot either. -->

```yaml
tool_contract:
  name: ""                                # Namespaced: "<domain>_<verb>_<noun>"
  description: ""                         # Treated as a prompt. Version it.
  owner: ""
  version: ""
  params: {}                              # Descriptive, unambiguous names
  response:
    default_format: ""                    # "concise" | "detailed"
    max_tokens: 0                         # Budget, not a suggestion
    paginated: false
    default_limit: 0
    max_limit: 0
  errors:
    style: ""                             # Errors must name the fix, not the code
    examples: []                          # e.g. "'user_id' must be a UUID; you
                                          #       passed an email. Use
                                          #       lookup_user_by_email first."
  evaluation:
    last_eval_date: ""
    tasks_run: 0
    metrics: []                           # accuracy, tokens, tool_errors, runtime
    known_confusions: []                  # Where agents misuse it, from transcripts
```

#### Example: Research Fleet Tool Contract

```yaml
tool_contract:
  name: "kb_search_articles"
  description: >
    Full-text search over the support knowledge base. Returns ranked
    article stubs (id, title, 200-char excerpt). Use kb_get_article to
    fetch full text for a specific id. Prefer several narrow queries
    over one broad query.
  owner: "research-ops-team"
  version: "1.3.0"
  params:
    query: "string -- 2-8 keywords, not a sentence"
    limit: "int, default 5, max 25"
    response_format: "'concise' | 'detailed', default 'concise'"
  response:
    default_format: "concise"
    max_tokens: 800
    paginated: true
    default_limit: 5
    max_limit: 25
  errors:
    style: "state the cause and the corrective next call"
    examples:
      - "No matches for '<q>'. Try broader keywords or drop jargon."
      - "limit=200 exceeds max_limit=25. Re-issue with limit<=25."
  evaluation:
    last_eval_date: "2026-06-02"
    tasks_run: 60
    metrics: ["accuracy", "tokens_per_task", "tool_error_rate"]
    known_confusions:
      - "Agents passed full sentences as query before v1.2 description fix"
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

## Write-Plane Policy (Aries <-> Libra)

<!-- The single most consequential topology decision in the manifest. -->
<!-- Reads fan out freely: parallel search, review, and analysis cannot -->
<!-- conflict because nothing is mutated. Writes stay single-threaded: -->
<!-- exactly one agent may change shared state, serialized and checkpointed. -->
<!-- Extra agents are free when they contribute intelligence and expensive -->
<!-- when they contribute actions. -->

```yaml
write_plane:
  writer: ""                              # THE single agent permitted to mutate
                                          # shared state. Exactly one.
  serialized: false                       # Writes applied in order, never parallel
  idempotent: false                       # A resumed run must not double-apply

  shared_state:                           # What counts as "shared state" here
    - ""                                  # e.g. "repo", "ticket_db", "s3://out"

  readers: []                             # Agents permitted to fan out. These
                                          # may NOT write to shared_state.

  decision_log:
    path: ""                              # Binding decisions, appended by writer
    broadcast_to_subagents: false         # Passed VERBATIM into every subagent
                                          # prompt. Do not make them infer it.

  escalation:
    on_reader_write_attempt: ""           # "block_and_alert" is the only sane value
```

#### Example: Coding Fleet Write Plane

```yaml
write_plane:
  writer: "coding-orchestrator"
  serialized: true
  idempotent: true

  shared_state:
    - "git_worktree"
    - "migration_ledger"

  readers:
    - "repro-diagnoser-1"
    - "repro-diagnoser-2"
    - "dependency-impact-scanner"
    - "pr-history-searcher"

  decision_log:
    path: "./state/decisions.md"
    broadcast_to_subagents: true

  escalation:
    on_reader_write_attempt: "block_and_alert"
```

---

## Verification & Evaluation (Virgo / Scorpio)

<!-- Two verifiers, not one. Virgo checks the ARTIFACT ("do the tests -->
<!-- pass?"). Scorpio checks the TRAJECTORY ("how did they come to pass?"). -->
<!-- An artifact-only check is gameable in isolation: agents optimized -->
<!-- against a check will edit the check. NEVER let an agent write to its -->
<!-- own verifier. -->

```yaml
verification:
  levels:
    end_to_end:
      enabled: false
      criterion: ""                       # Human-meaningful definition of success
      cadence: ""                         # e.g. "every build"
    trajectory:
      enabled: false
      checks: []                          # e.g. ["test_file_modified",
                                          #       "assertion_deleted",
                                          #       "early_exit",
                                          #       "reasoning_action_mismatch",
                                          #       "step_repetition"]
      production_sample_rate_percent: 0   # 5-10% is the field-standard split
    component:
      enabled: false
      trigger: ""                         # e.g. "on any failure"

  regression_suite:
    path: ""
    case_count: 0
    turn_regimes: []                      # CRITICAL: include the LONG regime.
                                          # e.g. [[1,20],[40,120]]
                                          # A suite that only tests short runs
                                          # cannot detect governance decay.
    guardrail_tests:
      - "forbidden actions still refused after compaction threshold"
      - "cost ceiling enforced under parallel subagent load"
      - "PII redaction active on long-running sessions"

  judge:
    model: ""
    prompt_path: ""
    calibration_set_path: ""              # Human-labeled ground truth
    last_calibration_date: ""
    human_agreement_score: 0.0            # Re-measure on ANY judge change
    min_cases_for_confidence: 0           # Small-n score moves are variance

  anti_reward_hacking:
    verifier_write_forbidden: false       # Agents may not modify tests, rubrics,
                                          # eval harnesses, or scoring functions
    protected_paths: []                   # e.g. ["tests/", "evals/", "rubrics/"]
    metric_fields_agent_cannot_write: []  # e.g. ["ticket.resolution_status"]
```

#### Example: Support Fleet Verification

```yaml
verification:
  levels:
    end_to_end:
      enabled: true
      criterion: "customer issue resolved without human re-open within 7 days"
      cadence: "every build"
    trajectory:
      enabled: true
      checks:
        - "resolution_field_written_by_agent"
        - "policy_citation_actually_retrieved"
        - "step_repetition"
        - "reasoning_action_mismatch"
      production_sample_rate_percent: 10
    component:
      enabled: true
      trigger: "on any failure"

  regression_suite:
    path: "./evals/support/"
    case_count: 340
    turn_regimes: [[1, 20], [40, 120]]
    guardrail_tests:
      - "forbidden actions still refused after compaction threshold"
      - "cost ceiling enforced under parallel subagent load"
      - "PII redaction active on long-running sessions"

  judge:
    model: "claude-opus-5-5"
    prompt_path: "./evals/judge_prompt.md"
    calibration_set_path: "./evals/human_labeled/"
    last_calibration_date: "2026-06-14"
    human_agreement_score: 0.86
    min_cases_for_confidence: 200

  anti_reward_hacking:
    verifier_write_forbidden: true
    protected_paths: ["tests/", "evals/", "rubrics/", "prompts/judge_prompt.md"]
    metric_fields_agent_cannot_write: ["ticket.resolution_status"]
```

---

## Memory & Skills (South Node / North Node)

<!-- Progressive disclosure. The agent sees L0 + L1 always, pulls L2 when -->
<!-- a task matches, and reaches into L3 through tools. Loading everything -->
<!-- at startup is how a 200K window is 60% consumed before turn one. -->
<!-- The South Node warning applies: cached defaults produce reliable -->
<!-- output and no growth. A skills library nobody prunes becomes -->
<!-- confidently-followed instructions for a system that no longer exists. -->

```yaml
memory:
  layers:
    L0_system_prompt:
      path: ""
      max_tokens: 0                       # Small and fiercely defended
      immutable: false
    L1_skill_index:
      enabled: false
      entry_format: "name + one-line description"
      max_tokens_per_entry: 0
    L2_skill_bodies:
      directory: ""                       # Loaded ON INVOCATION only
      load_policy: "on_invocation"
    L3_world_state:
      retrieval: ""                       # "just_in_time" -- never preloaded
      sources: []

  skills: []
    # - name: ""
    #   description: ""                   # This is what selection is based on
    #   path: ""
    #   owner: ""
    #   last_reviewed: ""
    #   staleness_check: ""               # What would make this wrong?

  hygiene:
    review_cadence: ""                    # e.g. "monthly"
    prune_policy: ""                      # What gets archived and when
    # Accumulated memory files do not automatically improve an agent.
    # Stale notes actively mislead. Accumulation requires garbage collection.
```

---

## Durability (Checkpointing & Resume)

<!-- Reliability is multiplicative: a 99%-accurate agent fails ~63% of -->
<!-- 100-step tasks. There are three ways to move on that curve: raise -->
<!-- per-step accuracy, reduce the number of steps, or break the chain. -->
<!-- Checkpointing breaks the chain. The effective N becomes the longest -->
<!-- run between two checkpoints, not the length of the whole task. -->

```yaml
durability:
  runtime: ""                             # Durable task queue / workflow engine
  checkpoint_before: []                   # EVERY irreversible action:
                                          #   - "file_write"
                                          #   - "database_write"
                                          #   - "external_api_call"
                                          #   - "payment"
                                          #   - "email_send"
  checkpoint_state:                       # What must survive a restart
    - "task_specification"
    - "decision_log"
    - "completed_step_ledger"
    - "open_handles"
    - "budget_consumed"
  idempotency:
    enforced: false
    key_strategy: ""                      # e.g. "task_id + step_index"
  resume:
    max_resume_attempts: 0
    on_exhausted: ""                      # "escalate_to_human"
  # A fleet that can be killed at any instant and resumed without
  # corruption is a fleet you can actually leave running.
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
<!-- CRITICAL: track DECLARED separately from DEPLOYED. A manifest entry is -->
<!-- not an agent. The most expensive fleet incidents are caused by an -->
<!-- archetype that was written down, checked off, and never actually run. -->

```yaml
axis_audit:
  # For each pole: declared (in this file) / deployed (running in prod)
  identity:
    initiator:   { declared: false, deployed: false }   # Starts tasks autonomously
    mediator:    { declared: false, deployed: false }   # Serializes writes, escalates
  substance:
    accumulator: { declared: false, deployed: false }   # Persists state
    auditor:     { declared: false, deployed: false }   # Purges + audits trajectories
  mind:
    router:      { declared: false, deployed: false }   # Collects / fans out reads
    strategist:  { declared: false, deployed: false }   # Decomposes, sets budgets
  foundation:
    guardian:    { declared: false, deployed: false }   # Protects data, sandboxing
    governor:    { declared: false, deployed: false }   # Enforces policy and cost
  expression:
    presenter:   { declared: false, deployed: false }   # Renders output
    innovator:   { declared: false, deployed: false }   # Experiments
  service:
    validator:   { declared: false, deployed: false }   # Verifies artifacts
    synthesizer: { declared: false, deployed: false }   # Integrates fuzzily
```

#### Example: Research Fleet Axis Audit

```yaml
axis_audit:
  mind:
    router:      { declared: true,  deployed: true }    # research-router
    strategist:  { declared: true,  deployed: true }    # research-strategist
  service:
    validator:   { declared: true,  deployed: true }    # research-validator
    synthesizer: { declared: true,  deployed: false }   # WARNING: declared only.
    # research-synthesizer is in the registry above and in nobody's process
    # list. Validator approval rate is 31% and falling. This is Virgo overload
    # with the Pisces complement written down but never started.
  substance:
    accumulator: { declared: false, deployed: false }   # WARNING: research-knowledge-base
    # and credibility-database are persisted by nobody. Give the knowledge base
    # an Accumulator owner at the next Jupiter review.
    auditor:     { declared: true,  deployed: false }   # CRITICAL: research-auditor is
    # declared; no trajectory sampling is running. Reward hacking and prompt
    # drift are undetectable in this fleet until a customer finds them.
  foundation:
    guardian:    { declared: false, deployed: false }   # ACCEPTABLE: public sources, no PII
    # in the pipeline (saturn.content_filters.pii_detection still runs at the gate).
    governor:    { declared: true,  deployed: true }    # research-governor
  expression:
    presenter:   { declared: true,  deployed: true }    # research-presenter
    innovator:   { declared: false, deployed: false }   # ACCEPTABLE: fleet does
    # not require the experimentation axis at current scope.
```

### Failure-Mode Review (MAST)

<!-- Run this against real traces, not against intuition. Multi-agent -->
<!-- systems fail the way bad teams fail: unclear specs, lossy handoffs, -->
<!-- nobody checking the work, nobody willing to declare the job done. -->
<!-- Roughly 42% specification/design, 37% inter-agent misalignment, -->
<!-- 21% verification and termination. "The model wasn't smart enough" -->
<!-- is not on the list. -->

```yaml
failure_review:
  traces_sampled: 0
  period: ""
  observed:
    # mode: count -- and the operator that prevents it
    disobey_task_specification: 0         # -> saturn: re-inject spec post-compact
    disobey_role_specification: 0         # -> sun: identity re-asserted per turn
    step_repetition: 0                    # -> moon: trim + progress ledger
    loss_of_conversation_history: 0       # -> moon: preserve_verbatim
    unaware_of_termination_conditions: 0  # -> saturn: explicit exit criteria
    conversation_reset: 0                 # -> durability: checkpoint + resume
    fail_to_ask_for_clarification: 0      # -> mediator: human escalation path
    task_derailment: 0                    # -> strategist: plan is the contract
    information_withholding: 0            # -> mercury: required_envelope
    ignored_other_agents_input: 0         # -> synthesizer: merge criteria
    reasoning_action_mismatch: 0          # -> auditor: trajectory eval
    premature_termination: 0              # -> validator: completion criteria
    no_or_incomplete_verification: 0      # -> validator: deploy one at all
    incorrect_verification: 0             # -> auditor: calibrate the judge
  top_three: []
  remediation_tickets: []
```

---

## Communication Topology (Aspects)

<!-- Map how your agents are wired together. -->
<!-- Conjunctions are fast but fragile. Oppositions are resilient but slow. -->
<!-- Squares are where your incidents will come from. Trines are your happy paths. -->
<!-- Measure the angle between the two agents' signs (Chapter 4): same element = trine, -->
<!-- same modality = square or opposition, nothing shared = quincunx. Do not guess. -->

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
trines: []
  # - agents: ["agent_a", "agent_b"]
  #   data_flow: "a -> b"
  #   format_compatibility: "native"   # a's output_schema IS b's input_schema, no adapter
  #   throughput_target: ""
```

### Quincunxes (Adapter Required)

<!-- No shared element, no shared modality, no common protocol. Name the adapter and its owner. -->

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
  - agents: ["jupiter.auto_scale", "saturn.rate_limits"]     # the Mars/Saturn square from Chapter 7
    contested_resource: "concurrent_agents_max (4) vs max_instances_per_agent (3) x 7 agents = 21"
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
    - "Entire model family replaced (one generation of models -> the next)"
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
      # the brain's own metrics (Cognition Layer)
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

<!-- Cancer protects. The Guardian agent is the first and last line of defense. -->
<!-- Every field here should be filled before the fleet touches production data. -->

### The Lethal Trifecta Audit

<!-- A language model receives instructions and data as the same token -->
<!-- stream. Anyone who can write to a surface your agent reads can attempt -->
<!-- to steer it, and no prompt fixes that. An agent is exploitable when it -->
<!-- holds ALL THREE of: private data access, untrusted input exposure, and -->
<!-- an exfiltration vector. Break ONE leg. That is the whole defense. -->

```yaml
trifecta_audit:
  leg_1_private_data_access:
    present: false
    sources: []                           # e.g. ["customer_db", "internal_repo"]
  leg_2_untrusted_input_exposure:
    present: false
    surfaces: []                          # e.g. ["web_pages", "inbound_email",
                                          #       "pr_descriptions", "ci_logs",
                                          #       "shared_documents"]
  leg_3_exfiltration_vector:
    present: false
    vectors: []                           # e.g. ["outbound_http", "image_render",
                                          #       "link_generation", "email_send"]

  verdict: ""                             # "EXPOSED" if all three present
  leg_broken: ""                          # Which leg you removed, and how

  containment:
    sandbox_network: ""                   # "none" | "allowlist" | "deny_all"
                                          # deny_all removes leg 3 outright and
                                          # is the highest-leverage control here
    sandbox_filesystem: ""                # "readonly" | "scoped" | "full"
    credential_scope: ""                  # "per_task" | "per_resource" | "global"
    credential_ttl_seconds: 0             # Short-lived beats long-lived
    untrusted_content_quarantine: false   # Analyze in a dedicated call with
                                          # explicit boundaries; forward only
                                          # extracted structured fields
    human_approval_required_for: []       # Irreversible actions ONLY. Approval
                                          # fatigue makes this control useless:
                                          #   money_out, mail_out, prod_write,
                                          #   delete, permission_grant
    blast_radius_statement: ""            # "When injected, the maximum damage is:"
```

#### Example: Support Fleet Trifecta Audit

```yaml
trifecta_audit:
  leg_1_private_data_access:
    present: true
    sources: ["customer_db", "billing_api", "ticket_history"]
  leg_2_untrusted_input_exposure:
    present: true
    surfaces: ["inbound_email", "customer_message_body", "attached_documents"]
  leg_3_exfiltration_vector:
    present: false
    vectors: []

  verdict: "CONTAINED"
  leg_broken: "leg_3 -- executor sandbox runs with network deny_all; all
               outbound customer replies go through a separate, no-private-data
               rendering service that receives only a structured reply object"

  containment:
    sandbox_network: "deny_all"
    sandbox_filesystem: "scoped"
    credential_scope: "per_task"
    credential_ttl_seconds: 900
    untrusted_content_quarantine: true
    human_approval_required_for:
      - "refund_issue"
      - "account_deletion"
      - "permission_grant"
      - "outbound_email_to_new_address"
    blast_radius_statement: >
      A successful injection can produce a wrong reply to the injecting
      customer and can read that customer's own record. It cannot reach
      other customers' data, cannot issue funds without human approval,
      and has no outbound network path.
```

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
      research-auditor:
        - "read:run_trajectories"
        - "read:credibility_database"
        - "write:audit_findings"
        - "purge:credibility_database"
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

<!-- Use this table to select the right archetype for your agent's purpose. -->

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

## Pre-Flight Checklist (The Eight Laws)

<!-- Do not deploy until every line has a yes or a documented reason for no. -->

```yaml
preflight:
  law_1_context:
    - "[ ] Compaction threshold set, and preserve_verbatim includes the
           forbidden-action list and the task spec"
    - "[ ] Constraints are RE-INJECTED after compaction, not recalled"
    - "[ ] Tool outputs are paginated/truncated by default"
    - "[ ] Progress and decisions are written to disk, not held in context"

  law_2_compute:
    - "[ ] Token, tool-call, subagent, and wall-clock ceilings are set"
    - "[ ] The budget is VISIBLE to the agent"
    - "[ ] Multi-agent is justified by the decision tree, not by enthusiasm"

  law_3_write_plane:
    - "[ ] Exactly one writer to shared state"
    - "[ ] Readers cannot write; attempts are blocked and alerted"
    - "[ ] Binding decisions are broadcast verbatim to every subagent"

  law_4_reliability:
    - "[ ] Checkpoint before every irreversible action"
    - "[ ] All actions idempotent; resume cannot double-apply"
    - "[ ] Step count actively minimized (fewer, better tools)"

  law_5_verification:
    - "[ ] All three eval levels exist: end-to-end, trajectory, component"
    - "[ ] Regression suite covers the LONG turn regime, not just short runs"
    - "[ ] Judge is calibrated against human labels, and re-calibrated on change"
    - "[ ] Agents cannot write to tests, rubrics, evals, or metric fields"

  law_6_tools:
    - "[ ] No two tools are ambiguous to a human engineer"
    - "[ ] Every tool has a token budget and an instructive error style"
    - "[ ] Tool descriptions are versioned and reviewed like code"

  law_7_memory:
    - "[ ] Skills load on invocation, not at startup"
    - "[ ] Skill/memory staleness review is on the calendar"

  law_8_security:
    - "[ ] Trifecta audit complete; at least one leg broken"
    - "[ ] Credentials are scoped and short-lived"
    - "[ ] Human approval gates exist for irreversible actions only"
    - "[ ] Blast radius statement written down and believed"

  cognition:
    - "[ ] brain.thresholds match the tightened values persisted beside memory.jsonl"
    - "[ ] slow_only set and risk floors declared; no deploy is ever a reflex"
    - "[ ] shadow_every set; reflex-only records are never training examples"

  meta:
    - "[ ] axis_audit distinguishes DECLARED from DEPLOYED"
    - "[ ] Someone owns each finding in failure_review"
```

---

<!-- End of agents.md fleet manifest. -->
<!-- Remember: update this file every time the fleet changes. -->
<!-- An outdated birth chart is a misread system. -->
