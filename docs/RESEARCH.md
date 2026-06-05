# 🔬 GuitarMo — Research Review

A curated literature review grounding each stage of GuitarMo in the academic
work it is based on. For every stage we note **(a)** the canonical methods,
**(b)** what GuitarMo does *today* (Phase 1, rule-based), and **(c)** the
data-driven / SOTA direction taken in later phases.

> This positions GuitarMo in the lineage of *query-by-humming*, *automatic music
> transcription (AMT)*, *automatic harmonization*, and *guitar arrangement /
> fingering* research.

---

## 1. Pitch tracking & melody extraction

**Methods.** Monophonic f0 estimation began with autocorrelation/cepstrum
methods and matured with **YIN** (de Cheveigné & Kawahara, 2002), whose
probabilistic extension **pYIN** (Mauch & Dixon, 2014) adds voiced/unvoiced
probabilities. Deep models now lead: **CREPE** (Kim et al., 2018) regresses
pitch directly from the waveform; **Melodia** (Salamon & Gómez, 2012) extracts
melody from *polyphonic* audio via pitch-contour characteristics.

**GuitarMo today.** pYIN via librosa, with voiced-probability gating for note
segmentation (`pitch.py`).

**Direction.** Phase 2 adds CREPE and **basic-pitch** (Bittner et al., 2022) as
pluggable backends and benchmarks them.

## 2. Note segmentation & rhythm quantization

**Methods.** Turning an f0 curve into discrete notes is part of **automatic
music transcription** (overview: Benetos, Dixon, Duan & Ewert, 2019). Tempo and
beats: dynamic-programming beat tracking (Ellis, 2007; librosa) and the
**madmom** RNN/DBN trackers (Böck et al., 2016).

**GuitarMo today.** Median-pitch segmentation with gap tolerance, librosa beat
tracking, and grid quantization to eighth notes (`transcribe.py`).

**Direction.** Phase 2 integrates madmom onsets/beats and meter estimation.

## 3. Key finding

**Methods.** The **Krumhansl–Schmuckler** algorithm correlates a pitch-class
histogram with perceptual tonal profiles (Krumhansl & Kessler, 1982; Krumhansl,
1990), revisited by Temperley (1999).

**GuitarMo today.** Duration-weighted pitch-class histogram correlated against
the 24 rotated Krumhansl–Kessler profiles (`key.py`).

## 4. Automatic harmonization (melody → chords)

**Methods.** The most directly relevant system is **MySong / Songsmith** (Simon,
Morris & Basu, 2008), which harmonizes a *sung* melody with a hidden-Markov
model — exactly GuitarMo's use case. Rule/expert systems trace back to
Ebcioğlu's **CHORAL** chorale harmonizer (1988). Probabilistic and tree-based
models (Paiement et al., 2006; Tsushima et al., 2017) and deep models —
**DeepBach** (Hadjeres et al., 2017) and triad-chord melody harmonizers (Yeh et
al., 2021) — define the modern landscape.

**GuitarMo today.** Transparent rule-based functional harmony with
difficulty-scaled vocabulary and cadence logic (`harmony.py`) — chosen as an
explainable baseline.

**Direction.** Phase 3 **trains** an HMM baseline (reproducing MySong) and a
neural seq2seq harmonizer, then A/B-tests against the rules.

## 5. Guitar arrangement & fingering

**Methods.** Optimal fingering is classically posed as a **shortest-path**
problem over fretboard positions (Sayegh, 1989; Radicioni et al., 2004).
Data-driven guitar modelling is enabled by **GuitarSet** (Xi et al., 2018) and
**DadaGP** (Sarmento et al., 2021), a large tokenized GuitarPro corpus.

**GuitarMo today.** DP melody fingering (least hand movement) with rule-based
chord voicings, melody on treble strings and harmony on bass strings
(`arrange.py`).

**Direction.** Phase 4 builds a full fretboard solver and learns idiomatic
voicings from GuitarSet/DadaGP.

## 6. Sound synthesis

**Methods.** The **Karplus–Strong** algorithm (Karplus & Strong, 1983), extended
by Jaffe & Smith (1983), is a minimal physical model of a plucked string; it
generalizes to **digital waveguide** synthesis (Smith, 1992).

**GuitarMo today.** Karplus–Strong nylon-string synthesis with a low-passed
excitation and light reverb — zero external binaries (`render.py`).

**Direction.** Phase 4 offers an optional physical-model/soundfont backend.

## 7. Difficulty grading & evaluation

**Methods.** Performance-difficulty estimation is an emerging MIR task; GuitarMo
encodes difficulty pragmatically as harmonic-rhythm + voicing + texture
complexity. Evaluation uses **mir_eval** (Raffel et al., 2014) for transcription
metrics.

**Direction.** Phase 6 adds a formal evaluation and a small user study.

## 8. Tooling

GuitarMo builds on **librosa** (McFee et al., 2015) and **music21** (Cuthbert &
Ariza, 2010).

---

## References

1. de Cheveigné, A., & Kawahara, H. (2002). *YIN, a fundamental frequency estimator for speech and music.* JASA 111(4).
2. Mauch, M., & Dixon, S. (2014). *pYIN: A fundamental frequency estimator using probabilistic threshold distributions.* ICASSP.
3. Kim, J. W., Salamon, J., Li, P., & Bello, J. P. (2018). *CREPE: A convolutional representation for pitch estimation.* ICASSP.
4. Salamon, J., & Gómez, E. (2012). *Melody extraction from polyphonic music signals using pitch contour characteristics.* IEEE TASLP 20(6).
5. Bittner, R. M., Bosch, J. J., Rubinstein, D., Meseguer-Brocal, G., & Ewert, S. (2022). *A lightweight instrument-agnostic model for polyphonic note transcription and multipitch estimation.* ICASSP.
6. Benetos, E., Dixon, S., Duan, Z., & Ewert, S. (2019). *Automatic music transcription: An overview.* IEEE Signal Processing Magazine 36(1).
7. Ellis, D. P. W. (2007). *Beat tracking by dynamic programming.* Journal of New Music Research 36(1).
8. Böck, S., Korzeniowski, F., Schlüter, J., Krebs, F., & Widmer, G. (2016). *madmom: A new Python audio and music signal processing library.* ACM Multimedia.
9. Krumhansl, C. L., & Kessler, E. J. (1982). *Tracing the dynamic changes in perceived tonal organization in a spatial representation of musical keys.* Psychological Review 89(4).
10. Krumhansl, C. L. (1990). *Cognitive Foundations of Musical Pitch.* Oxford University Press.
11. Temperley, D. (1999). *What's key for key? The Krumhansl–Schmuckler key-finding algorithm reconsidered.* Music Perception 17(1).
12. Simon, I., Morris, D., & Basu, S. (2008). *MySong: Automatic accompaniment generation for vocal melodies.* ACM CHI.
13. Ebcioğlu, K. (1988). *An expert system for harmonizing four-part chorales.* Computer Music Journal 12(3).
14. Paiement, J.-F., Eck, D., & Bengio, S. (2006). *Probabilistic melodic harmonization.* Canadian AI.
15. Tsushima, H., Nakamura, E., Itoyama, K., & Yoshii, K. (2017). *Function- and rhythm-aware melody harmonization based on tree-structured parsing and split-merge sampling of chord sequences.* ISMIR.
16. Hadjeres, G., Pachet, F., & Nielsen, F. (2017). *DeepBach: A steerable model for Bach chorales generation.* ICML.
17. Yeh, Y.-C., Hsiao, W.-Y., Fukayama, S., et al. (2021). *Automatic melody harmonization with triad chords: A comparative study.* Journal of New Music Research 50(1).
18. Sayegh, S. I. (1989). *Fingering for string instruments with the optimum path paradigm.* Computer Music Journal 13(3).
19. Radicioni, D., Anselma, L., & Lombardo, V. (2004). *A segmentation-based prototype to compute string instruments fingering.* Proc. Sound and Music Computing.
20. Xi, Q., Bittner, R. M., Pauwels, J., Ye, X., & Bello, J. P. (2018). *GuitarSet: A dataset for guitar transcription.* ISMIR.
21. Sarmento, P., Kumar, A., Carr, C., Zukowski, Z., Barthet, M., & Yang, Y.-H. (2021). *DadaGP: A dataset of tokenized GuitarPro songs for sequence models.* ISMIR.
22. Karplus, K., & Strong, A. (1983). *Digital synthesis of plucked-string and drum timbres.* Computer Music Journal 7(2).
23. Jaffe, D. A., & Smith, J. O. (1983). *Extensions of the Karplus–Strong plucked-string algorithm.* Computer Music Journal 7(2).
24. Smith, J. O. (1992). *Physical modeling using digital waveguides.* Computer Music Journal 16(4).
25. Raffel, C., McFee, B., Humphrey, E. J., et al. (2014). *mir_eval: A transparent implementation of common MIR metrics.* ISMIR.
26. McFee, B., Raffel, C., Liang, D., et al. (2015). *librosa: Audio and music signal analysis in Python.* SciPy.
27. Cuthbert, M. S., & Ariza, C. (2010). *music21: A toolkit for computer-aided musicology and symbolic music data.* ISMIR.

> Citations are provided for orientation and may contain minor bibliographic
> errors; verify against the original venues before formal use.
