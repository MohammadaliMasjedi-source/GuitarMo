# 🌟 GuitarMo — Vision, Quality Bar & Impact Plan

*How we take GuitarMo from "working MVP" to **paper-grade, presentation-grade,
and career-opening**.* This is the strategic companion to the
[ROADMAP](ROADMAP.md): the roadmap says *what* we build; this says *how good*,
*why it matters*, and *what doors it opens*.

---

## 1. North star

> A person sings; seconds later they hold a **beautiful, playable** classical-
> guitar arrangement at a difficulty they chose — and the system can *prove*
> (with numbers and a study) that the arrangements are accurate, harmonically
> sound, and actually playable.

"Best quality" here means four bars are all met at once:
**Engineering · Research · Product · Communication.**

## 2. The scientific-paper angle

The rule-based MVP is *not* the novelty — it's the baseline. The publishable
story is the combination:

> **"Difficulty-controllable singing-to-guitar arrangement"** — a system that (a)
> transcribes a sung melody, (b) harmonizes it with a *trained, style- and
> difficulty-conditioned* model, and (c) renders a **playability-aware** guitar
> arrangement, evaluated with objective metrics *and* a user study on perceived
> playability across skill tiers.

Why this is credible and novel enough:
- **Sing→accompaniment** has a famous ancestor (Microsoft *MySong*, 2008) but
  little recent work that is *guitar-specific*, *difficulty-graded*, and *open*.
- **Difficulty control** (easy/normal/professional) as a first-class, evaluated
  axis is underexplored.
- **Playability** (fingering cost, hand span) tied to a *perceived-difficulty*
  user study is a concrete contribution.

**Venues (most realistic first):**
- **ISMIR Late-Breaking/Demo** or **NIME demo** — achievable now with the MVP +
  a clean demo and short paper.
- **Sound and Music Computing (SMC)** / **ISMIR full paper** — after Phase 3
  (trained harmonizer) + Phase 6 (evaluation + user study).
- A **blog post / arXiv preprint** any time — cite it, link it, build reputation.

**What a paper needs (drives Phases 2/3/6):** baselines (rules vs HMM vs neural),
held-out metrics (`mir_eval`, chord accuracy), a **user study** on playability
and musicality, ablations, and full **reproducibility** (seeds, configs, model
cards, released weights).

## 3. The presentation / demo angle

People remember a *live demo*, not slides.
- **The 30-second wow:** sing 4 bars on stage → guitar plays back instantly with
  selectable style/tier. Rehearse it until it's bulletproof.
- **A 60–90s screen-recorded video** (sing → tab → audio) for README, LinkedIn,
  the [[website]] and talk intros.
- **An interactive HTML deck** in the same style as the thesis defence deck
  (offline, keyboard-nav) — reuse that pattern.
- **Before/after audio**: the same melody at easy vs professional, and across
  styles — instantly communicates the difficulty axis.

## 4. Career leverage (short & long term)

**Short term**
- A polished **public demo** (Hugging Face Space) + a starred GitHub repo =
  immediate, linkable proof of full-stack ML/audio skill.
- Portfolio centrepiece on the **[[Website repo|Mo · MassJedi site]]**; a strong
  talking point in interviews and for the thesis defence (shows breadth beyond
  batteries).

**Long term**
- A **demo/paper** → conference attendance → network in MIR/audio-ML.
- A reusable **MIR + training pipeline** (transferable to the battery-thesis ML
  muscle and to **[[SincoTec context|SincoTec]]** signal work).
- Feeds the **[[CellSight commercial demo]]** monetization barbell
  (demo → consulting → product): proof you can ship a real, delightful AI product.

## 5. The quality bar (definition of "impressive")

| Pillar | Bar | Where |
|--------|-----|-------|
| **Engineering** | typed, tested (CI green), packaged on PyPI, pluggable backends | Phase 2/5 |
| **Research** | baselines + metrics + user study + reproducibility + model cards | Phase 3/6 |
| **Product** | hosted demo, in-browser tab/PDF, mobile capture, <10s round-trip | Phase 5 |
| **Communication** | killer README, demo video, deck, blog/preprint, citation | Phase 6 |

## 6. Do-this-next (highest leverage first)

1. **Record a real sung demo** + 60s video → drop into README and the website. *(days)*
2. **Phase 2.1 — CREPE backend** for accuracy that survives real singing. *(short)*
3. **Deploy a Hugging Face Space** so anyone can try it from a link. *(short)*
4. **Phase 3 — train the harmonizer** on the RTX-3090; this is the paper's core. *(weeks)*
5. **Phase 6 — small user study** on playability/musicality → the paper's evidence. *(weeks)*
6. **Write the demo paper** (ISMIR LBD / NIME) once 1–5 are in hand.

> Track all of this live in [PROGRESS.md](PROGRESS.md) and the dashboard. Every
> item above maps to a phase/sub-phase with a Definition of Done.
