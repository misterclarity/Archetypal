# Chapter 7: Agentology (The Fleet Architecture)

## Why This Isn't a Digression

If you have read this far, you have internalized a framework for understanding multi-operator systems: specialized execution contexts, typed operators, communication topologies, complementary pairing, and lifecycle events. You learned it by applying it to one system (yourself), but the patterns are general.

This chapter is where the framework pays professional dividends. Everything you've learned maps directly onto a problem you are likely already solving or will solve soon: **how to design, govern, and maintain autonomous AI agents**—and, in the second half of the chapter, how to build one agent's "brain" out of a fast model and a slow one. The transfer is direct:

- **Signs** become **Agent Role Archetypes**—the twelve fundamental specializations any fleet can draw from, and the label space a classifier routes into
- **Planets** become **Governance Functions**—the management operators that keep the fleet aligned, bounded, and alive
- **Aspects** become **Communication Topologies**—the inter-agent wiring that determines whether your fleet is a superconductive pipeline or a deadlocked mess
- **Axes** become **Agent Pairing Strategies**—the complementary pairs that prevent overspecialization and systemic fragility
- **Transits** become **Lifecycle Events**—the scheduled maintenance windows, version migrations, and architectural audits that keep the fleet evolving

A birth chart is a fleet manifest for one human system. An `agents.md` is a fleet manifest for an autonomous system you design. Same architecture. Different substrate. You already understand fleet architecture. This chapter is the deployment guide.

---

## The Twelve Agent Archetypes (Signs as Role Definitions)

Every agent in a fleet occupies a **functional niche**. Just as every sign represents a unique coordinate in the behavioral field, every agent archetype represents a unique execution profile. The twelve archetypes are not arbitrary categories—they emerge from the same Element × Modality grid that generates the zodiac. Each archetype is the sign you met in Chapter 2, wearing a job title:

| Sign | Chapter 2 nickname | Archetype | Call signature |
|---|---|---|---|
| ♈ Aries | The Spark | **Initiator** | `agent.spawn(task, priority=MAX, deps=NONE)` |
| ♉ Taurus | The Garden | **Accumulator** | `agent.persist(state, ttl=LONG, retry=TRUE)` |
| ♊ Gemini | The REST Client | **Router** | `agent.route(msg, channels=ALL, parallel=ON)` |
| ♋ Cancer | The Secure Kernel | **Guardian** | `agent.protect(data, acl=STRICT, encrypt=ON)` |
| ♌ Leo | The Renderer | **Presenter** | `agent.render(output, format=RICH, user=YES)` |
| ♍ Virgo | The Static Analyzer | **Validator** | `agent.validate(output, schema=ENFORCED)` |
| ♎ Libra | The Mirror | **Mediator** | `agent.negotiate(agents, consensus=REQUIRED)` |
| ♏ Scorpio | The Composter | **Auditor** | `agent.audit(logs, depth=FULL, purge=STALE)` |
| ♐ Sagittarius | The Inference Engine | **Strategist** | `agent.plan(goal, decompose=TRUE, horizon=FAR)` |
| ♑ Capricorn | The Production Server | **Governor** | `agent.enforce(policy, budget=STRICT)` |
| ♒ Aquarius | The Mesh Node | **Innovator** | `agent.experiment(approach=NOVEL, risk=OK)` |
| ♓ Pisces | The Event Bus | **Synthesizer** | `agent.synthesize(sources=ALL, fuzzy=TRUE)` |

The **Element** determines what the agent operates on. The **Modality** determines how it executes:

| | **Cardinal** (init) | **Fixed** (persist) | **Mutable** (transform) |
|---|---|---|---|
| **Fire** (energy → action) | Aries / Initiator | Leo / Presenter | Sagittarius / Strategist |
| **Earth** (structure) | Capricorn / Governor | Taurus / Accumulator | Virgo / Validator |
| **Air** (information → communication) | Libra / Mediator | Aquarius / Innovator | Gemini / Router |
| **Water** (emotion → state) | Cancer / Guardian | Scorpio / Auditor | Pisces / Synthesizer |

A **Cardinal** agent starts processes. A **Fixed** agent maintains them. A **Mutable** agent transforms them. A **Fire** agent acts on energy. An **Earth** agent structures. An **Air** agent moves information. A **Water** agent tracks internal state.

### Each Archetype Has a Native Operator

Every sign has a ruling planet—the operator it calls by default (the chart-ruler table in Chapter 6). In a fleet, that is the archetype's default governance function; in the brain built later in this chapter, it is the handler's default behavior:

```
 Initiator   (Aries)   -> VECTOR     Mediator    (Libra)       -> BIND
 Accumulator (Taurus)  -> BIND       Auditor     (Scorpio)     -> REFORMAT
 Router      (Gemini)  -> IO_STREAM  Strategist  (Sagittarius) -> MULTIPLY
 Guardian    (Cancer)  -> BUFFER     Governor    (Capricorn)   -> LIMIT
 Presenter   (Leo)     -> IDENTITY   Innovator   (Aquarius)    -> INTERRUPT
 Validator   (Virgo)   -> IO_STREAM  Synthesizer (Pisces)      -> DISSOLVE
```

Archetype names the agent; operator names the policy it runs. "Aries/Initiator" is an agent. "Mars" is what it does when it runs.

### Worked Example: The Research Fleet

Suppose you are building an autonomous research team. The goal: "Analyze emerging trends in quantum computing and produce a briefing document." Here is the fleet composition and message flow:

> **1. Sagittarius / Strategist** receives the goal. Decomposes it into sub-queries: "recent breakthroughs," "key researchers," "commercial applications," "technical barriers." Sets the research horizon and success criteria.
>
> **2. Gemini / Router** takes the sub-queries and dispatches them across multiple data sources in parallel—academic APIs, news feeds, patent databases, arxiv. Manages channel multiplexing and deduplication.
>
> **3. Virgo / Validator** receives each raw result. Checks source credibility, cross-references claims, flags contradictions, enforces citation schema. Rejects anything that fails the quality gate.
>
> **4. Pisces / Synthesizer** takes the validated fragments and merges them into a coherent narrative. Identifies cross-domain patterns. Bridges gaps between technical and commercial findings using fuzzy semantic matching.
>
> **5. Leo / Presenter** formats the final output—executive summary, key findings, visual charts, recommended actions. Optimizes for the human reader.

Five archetypes. One pipeline. Each agent does exactly what its sign dictates. (The manifest in `agents.md` adds a sixth, a Capricorn / Governor, because somebody has to own the budget—see Planetary Governance below.)

### Worked Example: The Customer Support Fleet

A production customer support system requires different archetypes:

> **Cancer / Guardian** handles PII detection and encryption before any user data enters the pipeline. **Gemini / Router** classifies the incoming ticket and routes it to the appropriate specialist agent. **Taurus / Accumulator** maintains the long-running conversation state and customer history. **Libra / Mediator** orchestrates multi-agent responses when a ticket requires input from billing, technical support, and account management simultaneously. **Virgo / Validator** checks every outgoing response for policy compliance, tone, and factual accuracy before delivery. **Pisces / Synthesizer** merges the billing, technical, and account fragments into one reply in one voice, and ships it at good-enough when the Validator's remaining objections are cosmetic. **Scorpio / Auditor** runs continuous anomaly detection on response quality metrics, flagging drift before it becomes a crisis. **Sagittarius / Strategist** plans multi-step resolutions when a ticket needs more than a canned reply. **Capricorn / Governor** holds the budget and policy envelope every other agent operates inside.

Nine archetypes. Each one addresses a specific failure mode that would exist if it were absent—and the Strategist, Governor, and Synthesizer complete the Mind, Foundation, and Service axes that the Six Axes section below says must be paired. The Identity axis is open on purpose: the Mediator orchestrates, but nothing in this fleet initiates—every task begins with a customer's ticket—so there is no Initiator to balance. Record that in the manifest's axis audit. A gap you have named is a decision; a gap you have not is a bug.

---

## Planetary Governance (Operators as Management Functions)

Archetypes define what agents *are*. Governance defines what agents *may do*. Every planetary operator from Chapter 3 maps to a specific management function in the fleet:

```
AGENT GOVERNANCE — PLANETARY OPERATOR MAPPING
================================================

  SUN     IDENTITY    -->  Slow Thread: Deliberation & Purpose Declaration
  MOON    BUFFER      -->  Fast Thread: Cached Reflexes & Context Persistence
  MERC    IO_STREAM   -->  Inter-Agent Messaging Protocol
  VEN     BIND        -->  Dependency Graph & Service Mesh
  MARS    VECTOR      -->  Task Execution & Retry Policy
  JUP     MULTIPLY    -->  Auto-Scaling & Load Distribution
  SAT     LIMIT       -->  Guardrails, Rate Limits, Cost Caps
  CHIRON  WONTFIX     -->  Known Limitations & Documented Workarounds
  URA     INTERRUPT   -->  Circuit Breakers & Fallback Paths
  NEP     DISSOLVE    -->  Graceful Degradation & Fuzzy Fallback
  PLU     REFORMAT    -->  Version Migration & Agent Retirement
  N.NODE  IMPORT      -->  Capability Roadmap (what the fleet keeps deferring)
  S.NODE  ARCHIVE     -->  Cached Defaults (what the fleet does on autopilot)
```

The Nodes are the fleet's growth vector: `ARCHIVE` lists what it already does on autopilot; `IMPORT` lists what it keeps deferring. Review both in the Jupiter cycle. In the brain below they become literal: `ARCHIVE` is the compiled cache of past decisions, `IMPORT` is the queue of inputs the cache cannot explain.

**An agent without a Sun is a process without a PID.** Every agent must declare its identity—a unique name, a purpose statement, a model version, and a tool manifest. This is non-negotiable. Unregistered agents are rogue processes.

**Saturn is the most critical operator in any production agent fleet.** Without `LIMIT`, agents scale without constraint, spend without budget, and generate without guardrails. Saturn defines the boundaries that make autonomy safe. Implement Saturn as code, not as a prompt. A model cannot be the thing that limits models. The Governor agent owns Saturn's configuration and reviews what Saturn escalates; the gate itself is a pure function that runs on every output.

### Worked Example: Saturn Governance in Practice

> A customer support fleet is processing tickets. The **Sagittarius / Strategist** agent begins generating overly ambitious resolution plans—multi-step workflows involving external API calls, database lookups, and proactive outreach. Token usage spikes. Cost per ticket triples.
>
> **Saturn's `LIMIT` operator** activates (the keys are the `saturn:` block of `agents.md`):
>
> ```
> saturn.enforce({
>   rate_limits:  { max_tokens_per_task: 4000, max_tool_calls_per_task: 5 },
>   cost_caps:    { max_cost_per_hour_usd: 12.00 },
>   escalation_policy: { on_budget_exceeded: "freeze_agent",
>                        escalation_channel: "slack:#support-fleet-alerts" },
>   forbidden_actions: ["external_api_call_without_approval", "database_write"]
> })
> ```
>
> The Strategist is throttled. Tasks exceeding the token budget are routed to the **Capricorn / Governor** for manual review. The fleet continues operating within its cost envelope. Saturn does not punish—Saturn *defines*.

### Worked Example: Mercury Messaging Protocol

> The **Gemini / Router** collects raw search results and must pass them to the **Virgo / Validator** for the quality gate. The payload shape is already declared by the agents themselves—the Router's `output_schema` *is* the Validator's `input_schema`, `raw_results.json`. Mercury defines how it travels (again, the keys are the manifest's `mercury:` block):
>
> ```
> mercury.protocol({
>   message_format: "json",
>   schema_registry: "./schemas/messages/",
>   schema_validation: true,
>   routing_strategy: "direct",
>   retry_on_delivery_failure: true,
>   max_delivery_retries: 3,
>   dead_letter_queue: "undeliverable_messages"
> })
> ```
>
> Every message between agents passes through Mercury's `IO_STREAM`. No agent speaks a private language. The protocol is the law.

The payload changes per hop. The **envelope** never does. Mercury's real job is the wrapper every hop shares—who sent it, when, what has already happened to it:

```
Envelope {
  id, ts, source          -- who sent it, when
  text                    -- raw payload (only the executing handler sees it)
  redacted                -- the Guardian's copy: what models and memory see
  trace: [ "mercury:wrap", "cancer:redact", "moon:classify(novelty=0.00)",
           "saturn:gate", "pisces:review", "virgo:run" ]
}
```

The trace is appended by every stage. It is the decision's stack trace, and it is what the Auditor reads.

---

## The Six Axes of Agent Pairing (Complementary Agent Strategies)

Every axis from Chapter 2 defines a **resilience pair**. An unbalanced fleet—one that overweights one pole of an axis—will develop the systemic equivalent of a personality disorder. The fix is always the same: invoke the complementary archetype.

```
THE SIX AXES OF AGENT BALANCE
================================================

  Initiator   <-- Identity -->    Mediator
  (act fast)                      (check impact)

  Accumulator <-- Substance -->   Auditor
  (persist)                       (purge/audit)

  Router      <-- Mind ------>    Strategist
  (collect)                       (synthesize)

  Guardian    <-- Foundation -->  Governor
  (protect)                       (enforce)

  Presenter   <-- Expression -->  Innovator
  (render)                        (experiment)

  Validator   <-- Service ----->  Synthesizer
  (verify)                        (integrate)
```

**Rule: Never deploy one pole without its complement.**

1. **Aries-Libra (Initiator-Mediator)**: Every autonomous action agent needs an orchestrator checking for side effects. An Initiator fleet without a Mediator will fire-and-forget into chaos.

2. **Taurus-Scorpio (Accumulator-Auditor)**: Every persistence layer needs a garbage collector. An Accumulator without an Auditor will hoard stale state until memory pressure kills the fleet.

3. **Gemini-Sagittarius (Router-Strategist)**: Every data collection agent needs a planning agent. A Router without a Strategist collects everything and synthesizes nothing.

4. **Cancer-Capricorn (Guardian-Governor)**: Every privacy agent needs a compliance agent. A Guardian without a Governor protects data but has no enforcement policy for violations.

5. **Leo-Aquarius (Presenter-Innovator)**: Every user-facing agent needs a system-level experimentation agent. A Presenter without an Innovator will optimize for today's format and never evolve.

6. **Virgo-Pisces (Validator-Synthesizer)**: Every strict validation agent needs a fuzzy integration agent. A Validator without a Synthesizer produces analysis paralysis—perfect verification of nothing shipped.

In a fleet, the axis says which agent to hire. In a brain, it says who reviews: when a decision is made as an Initiator, the review pass runs as the Mediator and asks the Mediator's one question. The twelve questions are the Quick Diagnostic table from Chapter 2; the brain section below turns them into code.

### Worked Example: The Virgo-Overloaded Fleet

> A content generation fleet has three Validator agents checking every output for factual accuracy, tone compliance, and format adherence. The approval rate drops to 12%. The pipeline stalls. Nothing ships.
>
> **Diagnosis**: Virgo overload. The system has maximized `LINT` without any `STREAM`.
>
> **Patch**: Deploy a **Pisces / Synthesizer** agent with a "good enough" threshold. The Synthesizer applies semantic similarity scoring—if 90% of validation criteria pass and the failures are cosmetic, the output ships with a soft warning tag instead of a hard block. The approval rate rises to 78%. The Validators still catch real errors. The Synthesizer prevents perfectionism from becoming paralysis.

---

## Aspect Topologies (Inter-Agent Communication Patterns)

The aspects from Chapter 4 map directly onto **inter-agent communication architectures**. The geometry between two agents determines the quality of their connection.

**Conjunction (0°)—Monolith / Tight Coupling**
Two agents merged into one process. Maximum coherence, minimum modularity. *Example*: An agent that both generates AND validates its own output. Fast, but impossible to scale or audit independently.

**Opposition (180°)—Distributed / Microservice**
Two agents at maximum separation, communicating over a network boundary. Maximum observability and independent scaling, but latency and serialization overhead. *Example*: A generation agent on one server and an evaluation agent on another, connected only by a message queue. Oppositions are the axis pairs: in a brain they review each other's decisions rather than hand work to each other.

**Square (90°)—Contention / Deadlock Risk**
Two agents competing for the same resource with incompatible optimization targets. *Example*: An Aries/Initiator agent optimizing for speed (its Mars `VECTOR` policy set to max priority) and a Capricorn/Governor agent optimizing for cost (enforcing the Saturn `LIMIT` policy)—both drawing on the same token budget. Cardinal Fire against Cardinal Earth: same lifecycle phase, incompatible strategy. Without an explicit concurrency protocol, they deadlock.

> **Resolving the Square**: Define a priority hierarchy. The `LIMIT` function sets the *ceiling*. The `VECTOR` function operates *within* the ceiling. The Governor publishes a budget. The Initiator draws from it. Contention becomes collaboration when the resource contract is explicit:
>
> ```
> resource_contract({
>   token_budget: saturn.get_limit(),
>   allocation: mars.request(tokens, priority),
>   conflict_resolution: "agent_b_wins",  // the Governor; Saturn sets the ceiling
>   audit_trail: true
> })
> ```

**Trine (120°)—Superconductive Pipeline**
Agents with natural data flow and zero impedance. Same element, compatible modalities. *Example*: A Sagittarius/Strategist (fire/mutable) feeding a Leo/Presenter (fire/fixed)—the strategic plan flows directly into creative presentation with no format translation required. Research becomes briefing becomes output.

> **Trine Pipeline in Practice**: Strategist outputs a structured plan with sections, key findings, and recommended actions. Presenter receives it and renders each section into formatted prose, charts, and executive summary. The data types are natively compatible. No adapter layer needed. Test it with schemas, not vibes: a hand-off is a trine only if A's output schema is B's input schema with no adapter. The sign angles tell you where you will be writing adapters.

**Quincunx (150°)—Integration Hell**
Two agents with no shared protocol, no common data format, and no natural communication path. *Example*: A vision model agent (processes images, outputs bounding boxes) and a structured-data agent (processes JSON, outputs database records). Making them collaborate requires a custom adapter—the astrological equivalent of learning a completely foreign language.

Run the Research Fleet through this lens and its real shape appears. Strategist → Router is Sagittarius → Gemini: an opposition, the Mind axis—the plan and the collection stare at each other across a queue. Router → Validator is Gemini → Virgo: both mutable, a square—breadth against correctness, the pipeline's natural incident source. Validator → Synthesizer is Virgo → Pisces: the Service axis again, an opposition. Synthesizer → Presenter is Pisces → Leo: a quincunx—narrative prose does not map onto a sectioned briefing without an adapter. The one trine in the fleet is Strategist → Presenter, Fire to Fire, which is why the plan's section structure can become the briefing's skeleton with no translation. The manifest in `agents.md` wires it exactly this way.

---

## The Agent Runtime (Transits as Lifecycle Events)

Chapter 5 introduced life milestones as scheduled maintenance windows. The same model applies to agent fleet lifecycle management. These are not optional. Skip them and your fleet degrades silently until catastrophic failure.

```
AGENT LIFECYCLE — SCHEDULED CYCLES vs. EVENT TRIGGERS
=======================================================

Month:    0        3        6        9        12     |  event-driven
          |        |        |        |        |      |
DEPLOY    o--------o--------o--------o--------o======|=================>
          |     JUPITER  JUPITER  JUPITER  SATURN    |  URANUS      PLUTO
          |     scale    scale    scale    annual    |  major       full
          |     review   review   review   audit     |  migration   replatform
          |                                   |      |  (trigger)   (trigger)
          |                              +---------+ |  +---------+ +---------+
          |                              | STRUCT  | |  | VERSION | | FULL    |
          |                              | AUDIT   | |  | UPGRADE | | REFORMAT|
          |                              | test()  | |  | migrate | | rebuild |
          |                              +---------+ |  +---------+ +---------+
Cadence:     quarterly x 3                 annual       on trigger   on trigger
```

**Jupiter Cycle (Quarterly Review)**—`MULTIPLY` check. Are the right agents scaling? Are capabilities expanding appropriately? Add new tools, broaden scope, increase throughput where warranted. Jupiter asks: "Where should we grow?"

**Saturn Cycle (Annual Audit)**—`LIMIT` check. Stress test every structural commitment. Are guardrails holding? Are cost caps respected? Are deprecated endpoints still in use? Saturn asks: "What fails under pressure?"

**Uranus Trigger (Major Migration)**—`INTERRUPT` event. When the current architecture can no longer serve the fleet's purpose, Uranus forces the version upgrade. New model release, new API version, new regulatory requirement. This is not optional maintenance—it is a forced fork.

**Pluto Trigger (Full Replatforming)**—`REFORMAT` event. When the entire underlying substrate changes. Model family replacement, infrastructure migration, complete architectural redesign. The old fleet is retired. The new fleet carries the same purpose in a different body.

### Worked Example: The Saturn Cycle Audit

> Month 12. The annual audit begins. The **Capricorn / Governor** agent runs the Saturn protocol across the entire fleet:
>
> - **Finding 1**: The Gemini/Router agent is still calling a deprecated search API endpoint. The endpoint returns 200 OK but the data is stale by 72 hours. **Silent failure.**
> - **Finding 2**: The Sagittarius/Strategist agent's system prompt has drifted—14 incremental edits over 6 months have introduced contradictory instructions. **Prompt rot.**
> - **Finding 3**: The Virgo/Validator agent's schema enforcement was disabled during a hotfix in month 3 and never re-enabled. Unvalidated outputs have been shipping for nine months. **Guardrail erosion.**
> - **Finding 4**: The fast classifier's `Router` label has drifted—agreement with the slow thread fell from 0.96 to 0.81 after a prompt edit in month 7, but its reflex threshold was never tightened. 3,400 misrouted tickets shipped on the fast path. **Reflex rot.**
>
> Each finding generates a mandatory remediation ticket. The Saturn cycle does not ask "should we fix this?" It asks "why was this not caught sooner?" The audit is the system keeping itself honest.

---

## Building the Brain: The Two-Speed Runtime

Everything above describes a fleet—many agents, one manifest. This section builds the smallest thing that is still a *mind*: one agent with two speeds. It is the part of the chapter you can run tonight, and it comes straight out of a single sentence in Chapter 3:

> *When the system encounters a familiar stimulus, the Moon fires a cached response before the Sun's conscious thread can run its own evaluation.*

That sentence is an architecture. Cognitive science calls the two halves System 1 and System 2; the book calls them the `BUFFER` and the `IDENTITY` operator. In code they become a **fast classifier** and a **slow deliberator**:

| Layer | Operator | Model | Latency | Cost | Job |
|---|---|---|---|---|---|
| The Moon | `BUFFER` | `claude-haiku-5-5`, effort `low` | well under a second | ~$0.10 per million input tokens | Pattern-match the input against cached history: *which archetype handles this, how sure am I, how risky is it?* |
| The Sun | `IDENTITY` | `claude-opus-5-5`, adaptive thinking | seconds | ~$4 per million input tokens | Deliberate when the Moon is unsure, the input is novel, or the stakes are high |

The Moon is not a cheaper Sun. It answers a *narrower* question—routing, not reasoning—and it only answers it when it has seen something similar before. Everything else goes to the Sun. The whole design is the policy that decides which is which, and that policy is Saturn's.

### The Architecture

```
 THE TWO-SPEED RUNTIME — ONE INPUT, TWO SPEEDS, ONE GATE
 ══════════════════════════════════════════════════════════════════════════

                    input
                      │
                      ▼
        ┌───────────────────────────┐
        │ MERCURY   IO_STREAM       │  normalize into one envelope
        │ CANCER    Guardian        │  redact PII before anything else sees it
        └─────────────┬─────────────┘
                      │
                      ▼
        ┌───────────────────────────┐   few-shot examples: the Sun's
        │ MOON      BUFFER  (fast)  │◄──── past decisions on similar ────┐
        │ claude-haiku-5-5          │      inputs, with their rules      │
        │ -> sign, confidence, risk │                                    │
        │    + novelty vs memory    │                                    │
        └─────────────┬─────────────┘                                    │
                      │                                                  │
                      ▼                                                  │
        ┌───────────────────────────┐                                    │
        │ SATURN    LIMIT           │  may the reflex act alone?         │
        │ reflex / verify / think   │                                    │
        └──────┬─────────────┬──────┘                                    │
       reflex  │             │  verify (low effort) or think (high)      │
               ▼             ▼                                           │
     ┌──────────────┐  ┌───────────────────────────┐                     │
     │ REFLEX       │  │ SUN       IDENTITY (slow) │                     │
     │ cached       │  │ claude-opus-5-5           │                     │
     │ decision     │  │ adaptive thinking         │                     │
     └──────┬───────┘  │ -> Decision + rule        │                     │
            │          └─────────────┬─────────────┘                     │
            │  every Nth reflex is   │                                   │
            │  shadow-checked here   │                                   │
            └─────────┬──────────────┘                                   │
                      ▼                                                  │
        ┌───────────────────────────┐                                    │
        │ SATURN    gate            │  forbidden action? too long?       │
        │ AXIS      complement      │  the opposite archetype asks       │
        │           review          │  its one question                  │
        └─────────────┬─────────────┘  (a rejected reflex -> URANUS:     │
                      ▼                 one re-run on the slow path)     │
        ┌───────────────────────────┐                                    │
        │ HANDLERS[sign]            │  one of twelve; hand-offs follow   │
        │ dispatch by aspect        │  the aspect between the two signs  │
        └─────────────┬─────────────┘                                    │
                      ▼                                                  │
        ┌───────────────────────────┐                                    │
        │ TAURUS    memory.jsonl    │────────────────────────────────────┘
        │ write-back (redacted)     │  the Sun's labels and rules become
        └─────────────┬─────────────┘  the Moon's examples
                      ▼
        SCORPIO   auditor: Moon-vs-Sun disagreement rate -> tightens Saturn
```

### The Label Space Is the Zodiac

A classifier needs classes. The twelve archetypes are the classes—and because they come from the Element × Modality grid, they are not twelve arbitrary buckets but a 4 × 3 matrix a small model can learn. **Element** answers *what kind of payload is this?* **Modality** answers *what lifecycle phase is being asked for?*

| | **Cardinal** — start something | **Fixed** — keep something going | **Mutable** — transform / hand off |
|---|---|---|---|
| **Fire** — act, produce | **Initiator**: "kick off the deploy" | **Presenter**: "write the summary" | **Strategist**: "plan the migration" |
| **Earth** — structure, resources | **Governor**: "is this within budget?" | **Accumulator**: "save this for later" | **Validator**: "check this against the schema" |
| **Air** — information | **Mediator**: "which option is fairer?" | **Innovator**: "try something different" | **Router**: "look this up / forward this" |
| **Water** — state, protection | **Guardian**: "redact the PII first" | **Auditor**: "why did this happen?" | **Synthesizer**: "merge these three reports" |

Every input the brain receives is one of these twelve requests, and each class has exactly one handler. The classifier's job is to name the handler. The deliberator's job is to name it *correctly* when naming it is hard. There is deliberately no thirteenth "unknown" label: a catch-all becomes a silent sink. Uncertainty is expressed through confidence and novelty instead, and inputs that stay novel are the North Node—candidates for a new handler at the next Jupiter review.

### What the Moon Returns

The fast path never free-writes. It returns a typed verdict, enforced by structured output:

```
Verdict {
  sign        : one of the twelve     -- which handler
  confidence  : 0.0 – 1.0             -- 0.85+ only when unambiguous
  risk        : low | medium | high   -- irreversible? money, PII, prod, others?
  rationale   : one sentence
}
```

Its prompt contains two things: the twelve role definitions, and the nearest past cases the Sun has already judged—retrieved from memory by similarity and pasted in as examples, each with the one-line rule the Sun wrote for it. That retrieval is the cache. (The reference implementation measures similarity by word overlap and rescans memory on every call; swap `Memory.similar` for an embedding index before the file grows past a few thousand records, and re-tune ν when you do—novelty is defined by whatever similarity you use.) A brand-new brain has an empty cache and sends almost everything to the Sun; after a few hundred decisions the Moon has precedents for most of what it sees. Two numbers are computed outside the model: **novelty** (how unlike anything in memory the input is) and the **risk floor**—every handler declares the minimum risk of what it does, and the Moon may raise a risk grade but never lower it below that floor. The Initiator floor is *medium*: no deploy is ever a reflex.

### Saturn's Routing Rule

Saturn reads the verdict and picks one of three bands. The Moon acts alone only in the first:

| Band | Conditions | Who decides | Effort |
|---|---|---|---|
| **Reflex** | archetype not in the slow-only set, `risk == low`, `confidence ≥ τ` (0.85), `novelty ≤ ν` (0.60) | the Moon | one cheap call |
| **Verify** | same, but `confidence` between 0.70 and τ | the Sun checks the Moon's draft | `low` |
| **Deliberate** | anything else: slow-only archetype, risk above low, confidence below 0.70, novel input | the Sun | `high` |

The **slow-only set** is Initiator, Auditor, Governor, Innovator and Strategist: anything that *starts*, *purges*, *sets policy*, *experiments* or *plans* thinks first. It is a set membership test, not a number. τ, ν and the verify floor (0.70) are the only three numbers in the rule, and the Auditor moves τ for you—in one direction only. (The shadow rate that feeds the Auditor is a separate dial; Sprint 0 below sets it.)

### What the Sun Returns

When the Sun runs it receives the envelope, the Moon's provisional verdict (so it can disagree with it explicitly), and the same retrieved precedents. It deliberates the way the Strategist plans—thesis, payload type, lifecycle phase, then the handler—and returns a `Decision`:

```
Decision {
  sign, action, response, risk, confidence, rationale,
  needs_human : bool         -- irreversible, costly, or affecting others
  rule        : string|null  -- "when <pattern> -> <archetype>":
                             --   one line the Moon can learn
}
```

A reflex produces the same shape, so everything downstream—the gate, the review, the handler, the memory record—is identical for both paths. The two speeds differ only in *who filled in the struct*. The `rule` field is the real training signal: a sentence written by the strong model to be read by the weak one, stored next to the example it came from.

### The Gate and the Complement Review

Every `Decision`, fast or slow, passes through Saturn's gate (forbidden actions and patterns, output length) and then through the **complement review**: the archetype on the opposite end of the axis asks its one question from Chapter 2. Saturn also meters the Sun itself: the hourly cap on slow calls is checked before any deliberation or shadow check, and a Sun that cannot run holds the input for a person.

| Decision made by | Reviewed by | The question |
|---|---|---|
| Initiator (Aries) | Mediator (Libra) | What is the cost of this action to the shared system? |
| Accumulator (Taurus) | Auditor (Scorpio) | What must be garbage-collected before more is stored? |
| Router (Gemini) | Strategist (Sagittarius) | What is the thesis? Is anything here that is not it? |
| Guardian (Cancer) | Governor (Capricorn) | What rule makes this protection repeatable and enforceable? |
| Presenter (Leo) | Innovator (Aquarius) | Does this output serve a system bigger than its own UI? |
| Validator (Virgo) | Synthesizer (Pisces) | Can this ship at 80%? Is the remaining 20% cosmetic? |
| Mediator (Libra) | Initiator (Aries) | What does the system itself want, independent of consensus? |
| Auditor (Scorpio) | Accumulator (Taurus) | What must be preserved before anything is purged? |
| Strategist (Sagittarius) | Router (Gemini) | Which data points contradict the thesis? |
| Governor (Capricorn) | Guardian (Cancer) | Who is harmed by enforcing this rule? |
| Innovator (Aquarius) | Presenter (Leo) | Does the experiment still deliver a usable output? |
| Synthesizer (Pisces) | Validator (Virgo) | Which merged claim would fail verification? |

The review has two tiers. First a deterministic rule—the reviewer's question written as code (the Auditor rejects an Accumulator decision that would store more than the cap; the Mediator rejects an Initiator decision that touches production without a human; the Strategist rejects a Router decision with nothing to route). Then, for anything above low risk—or whenever the reviewer has no rule yet; the reference ships rules for six of the twelve—one more cheap model call with the reviewer's system prompt. A failed review of a *slow* decision flips `needs_human` on. A failed review of a *reflex* is a Uranus interrupt: the reflex is discarded and the input is re-run once on the slow path. This is the six axes doing in software what Chapter 2 asked you to do by hand—never run one pole without its complement—and it and the shadow check are the two places in the loop where the fast path can be overruled in real time.

### The Learning Loop

Three mechanisms turn a two-speed router into something that improves:

1. **Write-back.** Every decision is appended to memory with its redacted text, the Moon's label, the final label, the Sun's rule, which path ran, and whether the two agreed. The Sun's records are the Moon's future examples; reflex-only records are kept for novelty scoring but never used as examples, so the Moon cannot train itself on its own guesses.
2. **Shadow checks.** Every Nth reflex (default: one in ten) is *also* sent to the Sun at low effort. If the Sun disagrees, the Sun's decision wins and the disagreement is logged with the confused pair of labels. This is Scorpio's continuous anomaly detection applied to the brain itself.
3. **Threshold tuning.** When more than 20% of the last ten shadow checks disagree (one step per ten, so every step rests on evidence no earlier step used), the Auditor raises τ by 0.02 and persists it beside the memory file. Only shadow checks count: a verify or deliberate decision that overrules the Moon is logged for the audit but never moves τ, because on those inputs the Moon was never trusted in the first place. The brain becomes more cautious exactly when its reflexes are proven unreliable—and never loosens on its own. Loosening is a human decision made during a maintenance window, which is the one asymmetry that keeps the cache from quietly becoming a South Node: battle-tested, cheap, and wrong.

### Aspects as Hand-off Modes

When one handler needs another—the Router hands results to the Validator, the Strategist to the Presenter—the aspect between their signs tells you how to wire the hand-off:

| Aspect | Signs | Hand-off mode |
|---|---|---|
| Conjunction (0°) | same sign | merged into one process; loop capped |
| Sextile (60°) / Trine (120°) | compatible / same element | direct, no adapter |
| Square (90°) | same modality, different element | arbitrated—re-gated by Saturn before it runs |
| Quincunx (150°) | nothing shared | adapter required; the Sun writes it |
| Opposition (180°) | the axis pair | never a hop—the pair only reviews |

In the reference implementation the Router hands to the Validator across a square (Saturn's gate runs a second time on the hand-off, and it proceeds because the Validator is not slow-only) and the Strategist hands to the Presenter across a trine (it just runs). A handler that named its quincunx partner would stop the chain and flag that the Sun must write the adapter (the reference stub emits the flag; wiring that Sun call is yours).

### Maintenance Windows for a Brain

| Transit | Cadence | What it does to the brain |
|---|---|---|
| Jupiter | quarterly | handler-usage histogram and high-novelty count: which archetypes are never invoked? Which inputs keep coming back novel—the North Node asking for a new handler? |
| Saturn | annually (or on every incident) | reflex accuracy audit: disagreement rate, most-confused labels, recommendation on τ |
| Pluto | on model replacement | rebuild memory from the last 500 Sun-labeled records; the cache is reborn with the new substrate |

### Model Selection

| Role in the brain | Model | Why |
|---|---|---|
| Moon classifier · complement reviewer | `claude-haiku-5-5`, effort `low` | cheapest, fastest, structured output; swap for a fine-tuned small model once memory holds tens of thousands of labeled examples |
| Sun deliberation · shadow checks | `claude-opus-5-5`, effort `high` (deliberate) or `low` (verify, shadow) | adaptive thinking is always on; effort is the dial; one model means one prompt-cache namespace |
| Saturn gate · risk floors · dispatch | no model | deterministic code; a model cannot be the thing that limits models |

A model change is a Uranus trigger (it is already in the manifest's `uranus_trigger` conditions): pin the IDs in `agents.md` and re-baseline the Moon's thresholds after every swap—the examples were compiled against the old reflexes.

### What It Costs

Illustrative numbers at first-party API rates (`claude-haiku-5-5` $0.10 / $0.50 per million input / output tokens; `claude-opus-5-5` $4 / $20), assuming a fast call of ~800 input + ~100 output tokens, a verify call of ~1,500 input + ~200 output, and a high-effort deliberation of ~1,500 input + ~2,000 output tokens (thinking tokens are output tokens, and at high effort they dominate), with 10,000 inputs a day:

| Design | Daily calls | Daily cost (illustrative) |
|---|---|---|
| Everything on the Sun | 10,000 deliberate | ~$460 |
| Two-speed, 70% reflex / 15% verify / 15% deliberate | 10,000 fast + 1,500 verify + 1,500 deliberate | ~$85 |
| … plus one-in-ten shadow checks of the reflexes | + 700 low-effort Sun calls | ~$92 |
| … with prompt caching on both system prompts | same | lower still, once the prompt exceeds the model's minimum cacheable prefix (confirm with `usage.cache_read_input_tokens > 0`) |

The brain's economics are the Moon's hit rate. That is why the learning loop matters more than the model choice, and why Jupiter's "where should we grow?" is a cost question.

### The Reference Implementation

The repository ships the whole thing as one file: [`brain/archetypal_brain.py`](https://github.com/misterclarity/Archetypal/blob/master/brain/archetypal_brain.py), with offline tests in `brain/test_brain.py`. Every class in it is named after the operator it implements, so the file reads as a table of contents for this section.

```
$ python brain/archetypal_brain.py --mock "validate this JSON: {\"ok\": true}"
input     : validate this JSON: {"ok": true}
moon      : Validator (virgo)  conf=0.80  risk=low  novelty=1.00
path      : SLOW — confidence 0.80 < 0.85
decision  : Validator → validator:mutable  conf=0.80  risk=low
complement: Synthesizer asks “Can this ship at 80%? Is the remaining 20%
            cosmetic?” → approved
output    : payload is valid JSON
trace     : mercury:wrap > cancer:redact > moon:classify(novelty=1.00)
            > sun:deliberate(effort=high) > saturn:gate > pisces:review
            > virgo:run

$ python brain/archetypal_brain.py --mock "validate this JSON: {\"ok\": true}"
input     : validate this JSON: {"ok": true}
moon      : Validator (virgo)  conf=0.90  risk=low  novelty=0.00
path      : FAST — cached pattern
decision  : Validator → validator:reflex  conf=0.90  risk=low
complement: Synthesizer asks “Can this ship at 80%? Is the remaining 20%
            cosmetic?” → approved
output    : payload is valid JSON
trace     : mercury:wrap > cancer:redact > moon:classify(novelty=0.00)
            > saturn:gate > pisces:review > virgo:run
```

(The `complement` and `trace` lines are each printed on one line; they are wrapped here to fit the page.)

The first call deliberates (nothing in memory looks like it); the second is a reflex, because the first one became a precedent. Without an API key the file runs in mock mode—keyword classifier, canned deliberator—so the control flow can be studied before it costs anything. Mock runs write to their own `memory.mock.jsonl`, and records labeled by the canned deliberator are never used as examples by a live brain.

**Sprint 0 checklist:**

1. `pip install anthropic`, run the tests, run the two commands above in mock mode.
2. Replace the twelve stub handlers with the actions your system actually performs. Keep their signatures; let a handler return `(text, next_sign)` when it hands work on.
3. Decide your slow-only set, your risk floors, your forbidden patterns and the deterministic review rules. Default to more caution than feels necessary; the auditor will tell you if it is too much.
4. Decide what happens when a model call fails. The reference degrades deterministically—a Moon failure becomes an untrusted verdict (slow path), a Sun failure holds the input for a person, a reviewer failure counts as a rejection—and never counts a failure as a disagreement. Your retry and circuit-breaker numbers belong in the manifest's Mars `retry_strategy` and Uranus `circuit_breaker` keys.
5. Go live with `shadow_every = 3` in `Policy` for the first week, then relax toward 10 as the disagreement rate settles. The tightened τ is persisted beside the memory file; copy it into `agents.md` after each maintenance window.
6. Put the thresholds, the slow-only set and the shadow rate into your `agents.md` under the Cognition Layer, so the manifest and the brain agree.

---

## The `agents.md` Boilerplate—Your Fleet Manifest

Every birth chart begins with a moment of incarnation—the exact time, place, and configuration that defines a system's initial state. Your agent fleet deserves the same precision.

The `agents.md` file is the birth chart of your agent system. It is both documentation and operational manifest—a single source of truth that declares every agent's identity, role, governance policy, communication topology, and lifecycle schedule. When a new engineer joins the team, they read `agents.md` first. When an incident occurs, the investigation starts at `agents.md`. When the fleet evolves, `agents.md` evolves with it.

The boilerplate follows the full Archetypal Operating System framework:

- **Fleet Identity (Sun)**—who this fleet is and why it exists
- **Agent Registry (The Twelve Archetypes)**—every agent's role, model, tier, tools, and execution policy
- **Governance Layer (Planetary Operators)**—Saturn guardrails, Mercury messaging, Jupiter scaling, Pluto retirement
- **Cognition Layer (Moon / Sun)**—the fast classifier, the slow thinker, Saturn's thresholds, and the learning loop
- **Agent Pairings (The Six Axes)**—complementary pairs for resilience
- **Communication Topology (Aspects)**—how agents are wired together, square by square
- **Lifecycle Schedule (Transits)**—when the fleet is audited, scaled, migrated, and replatformed
- **Monitoring (Moon/Buffer)**—state persistence, logging, alerting, and the brain's own metrics
- **Security (Cancer/Guardian)**—authentication, authorization, and data classification

The complete [`agents.md`](https://github.com/misterclarity/Archetypal/blob/master/agents.md) boilerplate is included in this repository. Copy it. Customize it. Deploy it as the living configuration document for your fleet. Update it every time the fleet changes—because an outdated manifest is worse than no manifest at all.

---

## From Self-Knowledge to System Design

The same patterns that govern your internal architecture govern any system you build. The Archetypal Operating System is not just introspective—it is **generative**. The chart you learned to read in six chapters is the manifest you write in the seventh, and the Moon-before-Sun reflex you learned to profile in yourself is the loop you deploy.

You are no longer just reading your own source code. You are writing the source code for autonomous systems that carry your architectural intelligence forward. The fleet you design reflects the patterns you understand. Master the archetypes, and you master the fleet.

`fleet.deploy(manifest="agents.md", architect="you")`
