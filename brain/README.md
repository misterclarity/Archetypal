# The Reference Brain

A runnable, single-file implementation of the two-speed "brain" described in Chapter 7 of
*Archetypal Operating System*. It exists so the chapter's architecture can be executed, not
just read.

| Book concept | Code | What it does |
|---|---|---|
| Mercury / `IO_STREAM` | `Mercury.wrap()` → `Envelope` | Every input becomes one typed message with a `trace` |
| Cancer / Guardian | `Cancer.redact()` | PII leaves the text before any model or memory sees it |
| Moon / `BUFFER` | `Moon.classify()` | Fast classifier (`claude-haiku-5-5`): archetype, confidence, risk; novelty computed against memory |
| Sun / `IDENTITY` | `Sun.deliberate()` | Slow deliberation (`claude-opus-5-5`, adaptive thinking); writes a `rule` the Moon can learn |
| Saturn / `LIMIT` | `Saturn.allows_reflex()`, `effort_for()`, `gate()` | Reflex / verify / deliberate bands; risk floors; forbidden patterns; budgets |
| The twelve signs | `HANDLERS` | The classifier's label space is the handler registry |
| The six axes | `Brain.complement_review()` | The opposite archetype asks its Chapter 2 question |
| Uranus / `INTERRUPT` | inside `Brain.handle()` | A reflex the review rejects is re-run once on the slow path |
| Aspects | `aspect()`, `Brain.dispatch()` | Hand-offs between handlers follow the angle between their signs |
| Taurus / Accumulator | `Memory` (`memory.jsonl`) | The Sun's labeled decisions become the Moon's examples |
| Scorpio / Auditor | `Auditor` | Shadow-checks reflexes, measures disagreement, tightens the threshold (from shadow checks only; persisted beside the memory file) |
| Transits | `Brain.maintain()` | Jupiter / Saturn / Pluto maintenance windows |

## Run it

```bash
pip install -r brain/requirements.txt
python brain/archetypal_brain.py "validate this JSON: {\"ok\": true}"
python brain/archetypal_brain.py --repl
python brain/archetypal_brain.py --stats
python brain/archetypal_brain.py --maintain saturn
```

Without an `ANTHROPIC_API_KEY` the brain runs in **mock mode**: a keyword classifier stands in for
the Moon and a canned deliberator for the Sun, so the whole control flow (reflex gating, the verify
band, shadow checks, Saturn escalation, complement review, aspect-based hand-offs, memory write-back,
maintenance windows) can be studied offline. Mock runs write to `memory.mock.jsonl`; records labeled
by the canned deliberator are never used as few-shot examples by a live brain. Pass `--live` to use a
stored `ant auth login` profile, or export a key to call the real models. `--stats`, the shadow-check
cadence and the hourly slow-call cap are all rebuilt from the memory file, so one-shot CLI runs behave
like a long-running process.

Run the offline tests:

```bash
python brain/test_brain.py
```

## The loop, in one screen

```
input ─► Mercury.wrap ─► Cancer.redact ─► Moon.classify ─► Saturn: which band?
                                                │                 │
                                   examples ◄───┘      ┌──────────┼───────────┐
                                   (Sun-labeled)    reflex     verify      deliberate
                                                       │      (Sun, low)   (Sun, high)
                                                       │          │            │
                                           every Nth ──┘          │            │
                                           shadow-checked         ▼            ▼
                                                       └──────► Saturn.gate ◄──┘
                                                                     │
                                                                     ▼
                                                           complement_review
                                                     (reject a reflex → Uranus:
                                                      one re-run on the slow path)
                                                                     │
                                                                     ▼
                                                      dispatch: HANDLERS[sign], then
                                                      hand-offs by aspect (trine: direct,
                                                      square: re-gated, quincunx: adapter)
                                                                     │
                                                                     ▼
                                                      Memory.append (redacted text, rule)
                                                      Auditor.record / compare
```

Three thresholds live in `Policy` and are the knobs you will actually tune:

- `reflex_confidence` (0.85): how sure the Moon must be before it may act alone.
- `verify_confidence` (0.70): below `reflex_confidence` but above this, the Sun checks the Moon's draft at low effort.
- `reflex_max_novelty` (0.60): how closely the input must resemble something the Sun has already judged.

Plus two sets: `slow_only` (archetypes that always deliberate: anything that starts, purges, sets
policy, experiments or plans) and `risk_floor` (the minimum risk of what a handler does; the Moon may
raise a risk grade but never lower it below the floor).

The Auditor raises `reflex_confidence` by 0.02 when the last ten shadow checks show the reflex wrong
more than 20% of the time (one step per ten, so stale evidence expires), persists the new value in a
`.policy.json` sidecar next to the memory file, and never lowers it. Verify and deliberate decisions
that overrule the Moon are logged but never tighten anything—on those inputs the Moon was never
trusted. That is the whole learning loop: the Sun's decisions and rules make the Moon's examples, the
Auditor keeps the Moon honest, and Saturn decides when the Moon is allowed to speak.

## Notes on the live calls

- The Sun call uses `client.beta.messages.parse` with `fallbacks="default"` (beta
  `server-side-fallback-2026-07-01`), so a safety-classifier decline is re-run on a fallback model
  inside the same request. If the whole chain refuses, the decision is held for a human.
- Both models return structured output via `output_format=<pydantic model>`; the Moon runs at
  `effort="low"`, the Sun at `effort="high"` (deliberate) or `"low"` (verify and shadow checks).
- Both system prompts carry an explicit `cache_control` breakpoint on the system block (a top-level
  marker would land on the varying user message instead). Caching only engages once the prompt exceeds
  the model's minimum cacheable prefix; confirm with `usage.cache_read_input_tokens > 0` on the second call.
- `max_tokens` is 16,000 on the Sun and 1,024 on the Moon because adaptive-thinking tokens count against
  it; a Sun call that still runs out of room is retried once at `effort="medium"`.
- API errors (`anthropic.APIConnectionError`, `anthropic.APIStatusError`, which covers rate limits after
  the SDK's own retries) degrade deterministically: the Moon returns an untrusted verdict, the Sun returns
  `None` and the input is held for a human, a reviewer failure counts as a rejection. None of these are
  ever counted as Moon-vs-Sun disagreements.
- Models and memory only ever see `env.redacted`; the raw payload reaches the executing handler only.
- Similarity is word-overlap (Jaccard) with a full scan per call; `Memory.similar` is the swap point for
  an embedding index once the file grows past a few thousand records.
