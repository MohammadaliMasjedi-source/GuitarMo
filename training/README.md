# training/ — trainable models (Phase 3+)

Scaffold for the **data-driven** parts of GuitarMo. This is intentionally a
skeleton with clear `TODO`s — it is filled in during
[Phase 3](../docs/phases/PHASE_3_harmonization_ml.md) (neural harmonizer) and
[Phase 4](../docs/phases/PHASE_4_arrangement.md) (arrangement models).

## Layout
```
training/
├── download_data.py   # fetch corpora (+ generate a synthetic sample)
├── preprocess.py      # raw -> tokenized melody/chord dataset + splits
├── model.py           # HMM baseline + neural seq2seq harmonizer
├── train.py           # training loop (PyTorch), runs on the RTX-3090 (ISSE)
├── evaluate.py        # metrics + A/B vs the rule-based baseline
└── configs/
    └── harmonizer_small.yaml
```

## Intended workflow (Phase 3)
```bash
pip install -r ../requirements-ml.txt
python download_data.py --sample            # small public-domain sample
python preprocess.py  --config configs/harmonizer_small.yaml
python train.py       --config configs/harmonizer_small.yaml
python evaluate.py    --checkpoint runs/latest --baseline rules
```

The resulting model plugs into `guitarmo/harmony.py` behind
`--harmonizer ml`. See [docs/DATASETS.md](../docs/DATASETS.md) for sources and
licensing.
