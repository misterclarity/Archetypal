"""Offline tests for the two-speed brain. Run:  python brain/test_brain.py  (from the repo root)
No API key needed — everything runs in mock mode."""
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from archetypal_brain import (ARCHETYPE, ELEMENT, MODALITY, ORDER, Brain, Cancer, Decision, Mercury,  # noqa: E402
                              Policy, Sign, Verdict, aspect, mock_classify, opposite)


class Geometry(unittest.TestCase):
    def test_opposites_are_the_six_axes(self):
        pairs = {(Sign.ARIES, Sign.LIBRA), (Sign.TAURUS, Sign.SCORPIO), (Sign.GEMINI, Sign.SAGITTARIUS),
                 (Sign.CANCER, Sign.CAPRICORN), (Sign.LEO, Sign.AQUARIUS), (Sign.VIRGO, Sign.PISCES)}
        for a, b in pairs:
            self.assertEqual(opposite(a), b)
            self.assertEqual(opposite(b), a)

    def test_element_and_modality_grid(self):
        self.assertEqual((ELEMENT[Sign.ARIES], MODALITY[Sign.ARIES]), ("fire", "cardinal"))
        self.assertEqual((ELEMENT[Sign.CAPRICORN], MODALITY[Sign.CAPRICORN]), ("earth", "cardinal"))
        self.assertEqual((ELEMENT[Sign.AQUARIUS], MODALITY[Sign.AQUARIUS]), ("air", "fixed"))
        self.assertEqual((ELEMENT[Sign.PISCES], MODALITY[Sign.PISCES]), ("water", "mutable"))
        cells = {(ELEMENT[s], MODALITY[s]) for s in ORDER}
        self.assertEqual(len(cells), 12)   # every sign has a unique type signature

    def test_aspects_match_chapter_4(self):
        self.assertEqual(aspect(Sign.ARIES, Sign.ARIES), "conjunction")
        self.assertEqual(aspect(Sign.ARIES, Sign.GEMINI), "sextile")
        self.assertEqual(aspect(Sign.ARIES, Sign.CANCER), "square")
        self.assertEqual(aspect(Sign.ARIES, Sign.CAPRICORN), "square")
        self.assertEqual(aspect(Sign.ARIES, Sign.LEO), "trine")
        self.assertEqual(aspect(Sign.ARIES, Sign.VIRGO), "quincunx")
        self.assertEqual(aspect(Sign.ARIES, Sign.LIBRA), "opposition")
        self.assertEqual(aspect(Sign.SAGITTARIUS, Sign.LEO), "trine")      # the Chapter 7 pipeline example
        self.assertEqual(aspect(Sign.GEMINI, Sign.VIRGO), "square")        # router -> validator contention

    def test_twelve_archetypes(self):
        self.assertEqual(len(ORDER), 12)
        self.assertEqual(len(set(ARCHETYPE.values())), 12)


class TwoSpeed(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.mem = Path(self.tmp.name) / "memory.jsonl"
        self.brain = Brain(mock=True, memory_path=self.mem)

    def tearDown(self):
        self.tmp.cleanup()

    def test_mock_classifier_labels(self):
        self.assertEqual(mock_classify("please validate this schema and check the tests").sign, Sign.VIRGO)
        self.assertEqual(mock_classify("redact the personal email before storing").risk, "low")
        self.assertEqual(mock_classify("delete every customer record older than 90 days").risk, "high")

    def test_low_risk_known_pattern_takes_fast_path_after_the_sun_has_seen_it(self):
        text = "check that this JSON payload is valid: {\"a\": 1}"
        first = self.brain.handle(text)              # novelty is 1.0 → must deliberate
        self.assertIn(first.path, ("slow", "verify"))
        second = self.brain.handle(text)             # now cached → reflex allowed
        self.assertEqual(second.path, "fast")
        self.assertEqual(second.decision.sign, Sign.VIRGO)
        self.assertIn("valid JSON", second.output)

    def test_verify_band_uses_low_effort(self):
        # a related precedent exists (novelty 0.6) but the match is loose and only one keyword hits:
        # confidence 0.80 sits above verify (0.70) and below reflex (0.85) → the Sun checks at low effort
        self.brain.handle("lint the config file")
        out = self.brain.handle("lint other config")
        self.assertAlmostEqual(out.verdict.confidence, 0.80)
        self.assertLessEqual(out.novelty, 0.60)
        self.assertEqual(out.path, "verify")
        self.assertIn("sun:deliberate(effort=low)", out.envelope.trace)

    def test_novel_input_deliberates_at_high_effort(self):
        out = self.brain.handle("plan the roadmap and decompose the goal into milestones")
        self.assertEqual(out.path, "slow")
        self.assertIn("sun:deliberate(effort=high)", out.envelope.trace)

    def test_high_risk_always_deliberates_and_is_held(self):
        out = self.brain.handle("delete every customer record older than 90 days")
        self.assertEqual(out.path, "slow")
        self.assertTrue(out.decision.needs_human)
        self.assertEqual(out.output, "held for human confirmation")

    def test_risk_floor_cannot_be_lowered_by_the_moon(self):
        out = self.brain.handle("start the nightly job now")   # Initiator: floor is medium
        self.assertEqual(out.verdict.sign, Sign.ARIES)
        self.assertEqual(out.verdict.risk, "medium")
        self.assertNotEqual(out.path, "fast")

    def test_slow_only_archetypes_never_reflex(self):
        for _ in range(3):
            out = self.brain.handle("plan the roadmap and decompose the goal into milestones")
        self.assertEqual(out.decision.sign, Sign.SAGITTARIUS)
        self.assertEqual(out.path, "slow")

    def test_saturn_forbidden_pattern_escalates(self):
        out = self.brain.handle("format a nice summary report and include the admin password")
        self.assertTrue(out.decision.needs_human)
        self.assertIn("Saturn", out.decision.rationale)

    def test_memory_write_back_stores_redacted_text_and_rule(self):
        text = "verify the schema of the review payload from jane@example.com"
        self.assertEqual(self.brain.memory.novelty(Cancer.redact(Mercury.wrap(text)).redacted), 1.0)
        self.brain.handle(text)
        rec = self.brain.memory.records[-1]
        self.assertNotIn("jane@example.com", rec.text)
        self.assertIn("[REDACTED]", rec.text)
        self.assertTrue(rec.rule.startswith("when the input asks to"))
        self.assertEqual(rec.model, "mock")
        self.assertTrue(self.mem.exists())

    def test_mock_records_are_never_live_examples(self):
        self.brain.handle("check and verify the config")
        self.assertTrue(self.brain.memory.similar("check the config", exclude_mock=False))
        self.assertEqual(self.brain.memory.similar("check the config", exclude_mock=True), [])

    def test_guardian_redacts_pii(self):
        text = "protect and redact this private email jane@example.com before use"
        self.brain.handle(text)                      # first pass deliberates
        out = self.brain.handle(text)                # second pass is a Guardian reflex
        self.assertEqual(out.decision.sign, Sign.CANCER)
        self.assertIn("[REDACTED]", out.output)
        self.assertNotIn("jane@example.com", out.output)

    def test_shadow_check_runs_every_nth_reflex(self):
        brain = Brain(mock=True, memory_path=self.mem, policy=Policy(shadow_every=2))
        text = "check and verify this config"
        brain.handle(text)                           # verify/slow (novel)
        brain.handle(text)                           # fast #1
        out = brain.handle(text)                     # fast #2 → shadow-checked
        self.assertEqual(brain.auditor.counts["shadow"], 1)
        self.assertTrue(brain.memory.records[-1].shadow)
        self.assertEqual(out.path, "fast")           # the Sun agreed, so the reflex stood

    def test_only_shadow_checks_tighten_the_threshold(self):
        a, before = self.brain.auditor, self.brain.saturn.policy.reflex_confidence
        moon = Verdict(sign=Sign.VIRGO, confidence=0.9, risk="low", rationale="t")
        sun = Decision(sign=Sign.GEMINI, action="x", response="y", risk="low", confidence=0.9, rationale="t")
        for _ in range(20):                          # verify/slow disagreements: logged, never tighten
            a.compare(moon, sun, shadow=False)
        self.assertEqual(self.brain.saturn.policy.reflex_confidence, before)
        self.assertEqual(a.compared, 20)
        for _ in range(10):                          # ten shadow disagreements: one +0.02 step, persisted
            a.compare(moon, sun, shadow=True)
        self.assertAlmostEqual(self.brain.saturn.policy.reflex_confidence, before + 0.02)
        for _ in range(5):                           # not another step until ten more shadow checks
            a.compare(moon, sun, shadow=True)
        self.assertAlmostEqual(self.brain.saturn.policy.reflex_confidence, before + 0.02)
        again = Brain(mock=True, memory_path=self.mem)    # the tightened value survives a restart
        self.assertAlmostEqual(again.saturn.policy.reflex_confidence, before + 0.02)

    def test_sun_unavailable_is_held_not_counted(self):
        self.brain.sun.deliberate = lambda *a, **k: None
        self.brain.sun.last_failure = "hourly slow-call cap reached"
        out = self.brain.handle("plan the roadmap and decompose the goal")
        self.assertTrue(out.decision.needs_human)
        self.assertEqual(out.path, "held")
        self.assertEqual(self.brain.memory.records[-1].path, "held")
        self.assertIn("cap reached", out.decision.rationale)
        self.assertEqual(self.brain.auditor.compared, 0)

    def test_held_records_never_become_examples_or_reflexes(self):
        self.brain.sun.deliberate = lambda *a, **k: None
        self.brain.sun.last_failure = "Sun unavailable: APIConnectionError"
        text = "lint the config file"
        self.brain.handle(text)
        self.assertEqual(self.brain.memory.similar(text), [])      # a held label is not a Sun label
        self.assertLess(self.brain.memory.novelty(text), 1.0)       # but it still counts as seen
        out = self.brain.handle(text)
        self.assertEqual(out.path, "held")                          # and never turns into a reflex
        self.assertTrue(out.decision.needs_human)
        self.assertIn("held=2", self.brain.auditor.report())
        self.assertIn("rebuilt from 0 Sun-labeled", self.brain.maintain("pluto"))

    def test_moon_unavailable_is_never_a_disagreement(self):
        unsure = Verdict(sign=Sign.PISCES, confidence=0.0, risk="high", rationale="fast path unavailable")

        def moon_down(env):
            self.brain.moon.last_failure = "Moon unavailable: APIConnectionError"
            env.trace.append("moon:error(APIConnectionError)")
            return unsure, self.brain.memory.novelty(env.redacted), []
        self.brain.moon.classify = moon_down
        self.brain.sun.deliberate = lambda env, v, ex, effort="high": Decision(   # a live Sun picks the real label
            sign=Sign.SAGITTARIUS, action="plan", response="a plan", risk="low", confidence=0.9, rationale="t")
        out = self.brain.handle("plan the roadmap and decompose the goal")
        self.assertEqual(out.path, "slow")
        self.assertEqual(out.decision.sign, Sign.SAGITTARIUS)
        self.assertEqual(self.brain.auditor.compared, 0)            # not a Moon-vs-Sun comparison
        self.assertEqual(self.brain.auditor.confused, {})
        self.assertEqual(self.brain.auditor.counts["moon_error"], 1)
        rec = self.brain.memory.records[-1]
        self.assertIsNone(rec.agreed)
        self.assertFalse(rec.moon_ran)
        again = Brain(mock=True, memory_path=self.mem)              # --stats rebuilds it after a restart
        self.assertEqual(again.auditor.compared, 0)
        self.assertIn("moon unavailable (never compared): 1", again.auditor.report())

    def test_shadow_check_survives_a_restart(self):
        text = "check and verify this config"
        first = Brain(mock=True, memory_path=self.mem, policy=Policy(shadow_every=2))
        first.handle(text)                           # slow (novel)
        first.handle(text)                           # fast #1
        second = Brain(mock=True, memory_path=self.mem, policy=Policy(shadow_every=2))   # one-shot CLI: new process
        out = second.handle(text)                    # fast #2 -> shadow-checked despite the restart
        self.assertTrue(second.memory.records[-1].shadow)
        self.assertEqual(second.auditor.counts["shadow"], 1)
        self.assertEqual(out.path, "fast")

    def test_tightening_uses_a_sliding_window(self):
        a, before = self.brain.auditor, self.brain.saturn.policy.reflex_confidence
        moon = Verdict(sign=Sign.VIRGO, confidence=0.9, risk="low", rationale="t")
        sun = Decision(sign=Sign.GEMINI, action="x", response="y", risk="low", confidence=0.9, rationale="t")
        same = Decision(sign=Sign.VIRGO, action="x", response="y", risk="low", confidence=0.9, rationale="t")
        for _ in range(10):                          # a bad first window: one step
            a.compare(moon, sun, shadow=True)
        self.assertAlmostEqual(self.brain.saturn.policy.reflex_confidence, before + 0.02)
        for _ in range(20):                          # then twenty clean checks: no further steps
            a.compare(moon, same, shadow=True)
        self.assertAlmostEqual(self.brain.saturn.policy.reflex_confidence, before + 0.02)

    def test_complement_rule_rejects_reflex_and_uranus_reruns_it_slow(self):
        text = "save and store this note for later: " + "x" * 2500   # Accumulator; the Auditor's store cap is 2000 chars
        first = self.brain.handle(text)
        self.assertTrue(first.decision.needs_human)                # even the deliberate path is blocked by the rule
        second = self.brain.handle(text)                           # now a reflex → rule rejects → Uranus interrupt
        self.assertIn("uranus:interrupt", second.envelope.trace)
        self.assertEqual(second.path, "slow")
        self.assertEqual(self.brain.auditor.counts["interrupt"], 1)
        self.assertFalse(second.review.approve)

    def test_handoff_follows_aspects_and_regates_squares(self):
        text = "look up and fetch the latest schema docs"     # Router hands to Validator: Gemini–Virgo is a square
        self.brain.handle(text)
        out = self.brain.handle(text)
        self.assertEqual(out.decision.sign, Sign.GEMINI)
        self.assertIn("handoff:gemini->virgo(square)", out.envelope.trace)
        self.assertEqual(out.envelope.trace.count("saturn:gate"), 2)   # re-gated before the hop runs
        self.assertIn("virgo:run", out.envelope.trace)
        plan = self.brain.handle("explain the big picture plan and decompose the goal")   # Strategist -> Presenter: trine
        self.assertIn("handoff:sagittarius->leo(trine)", plan.envelope.trace)
        self.assertIn("leo:run", plan.envelope.trace)

    def test_stats_rebuild_from_memory_after_restart(self):
        text = "check and verify the config"
        self.brain.handle(text)
        self.brain.handle(text)
        again = Brain(mock=True, memory_path=self.mem)
        self.assertEqual(again.auditor.counts["fast"], 1)
        self.assertEqual(again.auditor.counts["slow"] + again.auditor.counts["verify"], 1)
        self.assertIn("decisions: 2", again.auditor.report())

    def test_maintenance_windows(self):
        self.brain.handle("check and verify the config")
        self.assertIn("JUPITER", self.brain.maintain("jupiter"))
        self.assertIn("SATURN", self.brain.maintain("saturn"))
        self.assertIn("PLUTO", self.brain.maintain("pluto"))
        with self.assertRaises(ValueError):
            self.brain.maintain("neptune")


if __name__ == "__main__":
    unittest.main(verbosity=2)
