# Appendix: Legend and Glossary

Everything a chart printout can throw at you, in one place. The three glyph tables are the same ones you met in the Introduction; the glossary covers every astrological term the book uses and a few your chart tool will show you that the book deliberately skips.

## Glyph Legend

**Signs** — the coordinates (Chapter 1) and, in Chapter 7, the agent archetypes.

| Glyph | Sign | Degrees | Element / Modality | Chapter 7 archetype |
|---|---|---|---|---|
| ♈ | Aries | 0°–29° | Fire / Cardinal | Initiator |
| ♉ | Taurus | 30°–59° | Earth / Fixed | Accumulator |
| ♊ | Gemini | 60°–89° | Air / Mutable | Router |
| ♋ | Cancer | 90°–119° | Water / Cardinal | Guardian |
| ♌ | Leo | 120°–149° | Fire / Fixed | Presenter |
| ♍ | Virgo | 150°–179° | Earth / Mutable | Validator |
| ♎ | Libra | 180°–209° | Air / Cardinal | Mediator |
| ♏ | Scorpio | 210°–239° | Water / Fixed | Auditor |
| ♐ | Sagittarius | 240°–269° | Fire / Mutable | Strategist |
| ♑ | Capricorn | 270°–299° | Earth / Cardinal | Governor |
| ♒ | Aquarius | 300°–329° | Air / Fixed | Innovator |
| ♓ | Pisces | 330°–359° | Water / Mutable | Synthesizer |

**Operators** — the planets and points (Chapter 3). The last column is how long each one stays in a sign, which is also how "personal" its sign placement is.

| Glyph | Body | Operator | Changes sign every |
|---|---|---|---|
| ☉ | Sun | `IDENTITY` | ~1 month |
| ☽ | Moon | `BUFFER` | ~2.5 days |
| ☿ | Mercury | `IO_STREAM` | ~3–4 weeks |
| ♀ | Venus | `BIND` | ~4 weeks |
| ♂ | Mars | `VECTOR` | ~6–7 weeks |
| ♃ | Jupiter | `MULTIPLY` | ~1 year |
| ♄ | Saturn | `LIMIT` | ~2.5 years |
| ⚷ | Chiron | `WONTFIX` | 2–8 years (eccentric orbit) |
| ♅ | Uranus | `INTERRUPT` | ~7 years |
| ♆ | Neptune | `DISSOLVE` | ~14 years |
| ♇ | Pluto | `REFORMAT` | ~12–30 years |
| ☊ / ☋ | North / South Node | `IMPORT` / `ARCHIVE` | ~1.5 years |

**Aspects** — the circuits (Chapter 4).

| Glyph | Aspect | Angle | Circuit |
|---|---|---|---|
| ☌ | Conjunction | 0° | Merge — monolith |
| ⚹ | Sextile | 60° | Link — helper path |
| □ | Square | 90° | Block — deadlock |
| △ | Trine | 120° | Flow — superconductor |
| ⚻ | Quincunx | 150° | Shim — no shared ABI |
| ☍ | Opposition | 180° | Mirror — distributed pair |

**Other marks on a chart printout**: **ASC / AC** = Ascendant (the Rising sign) · **MC** = Midheaven · **DC / IC** = the points opposite the Ascendant and Midheaven · **℞** or **R** = retrograde · **1–12** around the wheel = houses · **⊗** = Part of Fortune (ignore).

## Glossary

- **Natal chart / birth chart** — the computed snapshot of every planet's position on the zodiac ring at your birth moment, from your birth place. Inputs: date, time, place. Your source code.
- **Zodiac** — the 360° ring along which planets are located, divided into twelve 30° signs. The address space.
- **Ecliptic** — the apparent yearly path of the Sun through the sky; the zodiac ring is laid out along it.
- **Sign** — a 30° segment of the ring: the execution context an operator is running in.
- **Degree** — an operator's exact offset within its sign (0–29°). `address = sign_base + degree`.
- **Element** — Fire (energy), Earth (structure), Air (information), Water (emotion/state). The data type an operator works on.
- **Modality** — Cardinal (init), Fixed (persist), Mutable (transform). The lifecycle phase.
- **Polarity** — signs alternate outward (Fire, Air) and inward (Earth, Water); a parity bit on the sign index.
- **Luminaries** — the Sun and Moon.
- **Personal / social / outer planets** — Mercury, Venus, Mars (fast, individual) / Jupiter, Saturn (medium) / Uranus, Neptune, Pluto (slow; sign shared by a whole cohort).
- **Big Three** — Sun, Moon, Rising. The base image.
- **Rising sign / Ascendant (ASC)** — the sign on the eastern horizon at your birth minute. Needs birth time and place. The public API.
- **Midheaven (MC)** — the highest point of the chart; public role and career. Not used in this book.
- **Chart ruler** — the planet that rules your Rising sign. `PID 1` (table in Chapter 6).
- **Rulership** — each sign has a home operator (Aries → Mars, etc.). "Native context" in this book.
- **House** — one of twelve numbered slices of the wheel, counted from the Ascendant; the life domain in which an operator executes. Deliberately not used here—treat as a v2 feature.
- **Cusp** — a boundary: between two signs, or between two houses. The Pisces–Aries cusp is the ring's wrap-around point.
- **Aspect** — the angle between two operators: the circuit type (Chapter 4).
- **Orb** — tolerance around the exact aspect angle; ~8° for ☌ ☍ □ △, ~5° for ⚹, ~3° for ⚻. Smaller orb = stronger circuit.
- **Transit** — where a planet is in the sky *now*, read against your natal positions. The runtime clock.
- **Return** — a transiting planet arriving back at its natal position: one full orbit (Chapter 5).
- **Retrograde (℞)** — a planet appearing to move backward from Earth's vantage. Read as the operator in review mode: internalized, re-processing. Optional for a first profile.
- **Nodes (☊ ☋)** — where the Moon's orbit crosses the ecliptic. North = `IMPORT`, South = `ARCHIVE`; always 180° apart, so tools often print only the North.
- **Chiron (⚷)** — small body between Saturn and Uranus; the permanently open ticket (Chapters 3 and 5).
- **Stellium** — three or more operators in the same sign: a hot cluster. You will see the word in chart tools.
- **Archetype (Chapter 7)** — a sign read as an agent role: the twelve cells of the Element × Modality grid as a label space and handler registry.
- **Two-speed brain (Chapter 7)** — a fast classifier (the Moon) in front of a slow deliberator (the Sun), with Saturn deciding which one answers.
