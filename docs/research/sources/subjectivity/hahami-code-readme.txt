# Detecting the Disturbance: A Nuanced View of Introspective Abilities in LLMs

This repository contains the official implementation and code for the **arXiv preprint** of our paper ["Detecting the Disturbance: A Nuanced View of Introspective Abilities in LLMs"](https://arxiv.org/pdf/2512.12411).

Our ["dataset"](https://huggingface.co/datasets/elyhahami/llama-introspection-complex-concepts) and ["steering vectors"](https://huggingface.co/elyhahami/llama-introspection-steering-vectors) are also available on huggingface.

## Key Findings

### 1. Binary Detection is a Methodological Artifact
We show that the binary detection paradigm ("Did you detect an injected thought?") used in prior work conflates introspection with a simpler phenomenon: injection-induced global logit shifts that bias models toward affirmative responses *regardless of question content*. Detection accuracy and control question bias correlate at **r = 0.999**, with near-zero net signal across all 40 layer–strength configurations. The model isn't detecting the injection—it's just more likely to say "YES" to everything.

### 2. Partial Introspection is Real
Despite the negative result above, we find robust evidence for partial introspection on tasks requiring *differential* sensitivity:
- **Sentence Localization:** Models identify which of 10 sentences received an injection at up to **88% accuracy** (vs. 10% chance), with certain concept–layer combinations reaching 100%.
- **Strength Comparison:** Models discriminate relative injection strengths at up to **83% accuracy** (vs. 50% chance), with larger strength gaps yielding higher accuracy—indicating graded sensitivity to perturbation magnitude.

These tasks are immune to the global logit shift confound: a uniform bias toward "YES" cannot tell you *which* sentence was injected or *which* injection was stronger.

### 3. Introspection is Layer-Dependent
These capabilities are confined to early-layer injections (L0–L5) and collapse to chance levels beyond ~layer 10. This creates a narrow critical window where introspection succeeds—early enough for downstream signal integration, but before residual stream recovery dynamics attenuate the perturbation.

### 4. A Mechanistic Account Explains Why
We provide a three-part mechanistic explanation for the layer dependence:
- **Attention-based detection:** All 32 attention heads at the layer immediately after injection achieve **100% localization accuracy**. The injection creates a highly salient anomaly that attention mechanisms immediately identify.
- **Gradual integration:** Logit lens analysis shows the correct prediction emerges gradually over ~15 layers of downstream computation. The model needs processing depth to convert a detected anomaly into an explicit prediction.
- **Residual stream recovery:** The network actively attenuates perturbations, with cosine similarity returning toward baseline and projection onto the injection direction decaying exponentially.

Late-layer injections fail because there simply isn't enough computational runway for integration to complete before recovery erases the signal.



## Repository Structure

```
├── code/
│   ├── experiments/          # Core experiment implementations
│   │   ├── main.py           # Main runner (localization, detection experiments)
│   │   ├── strength_comparison.py    # Strength comparison experiment
│   │   ├── position_detection.py     # Binary detection experiment
│   │   ├── mechinterp.py             # Mechanistic interpretability experiments
│   │   └── mechinterp_patching.py    # Activation patching experiments
│   ├── utils/                # Utility functions
│   │   ├── all_prompts.py            # All prompts used in experiments
│   │   ├── compute_concept_vector_utils.py  # Vector computation
│   │   ├── save_vectors.py           # Vector saving utilities
│   │   ├── inject_concept_vector.py  # Injection utilities
│   │   └── api_utils.py              # API utilities (GPT judges)
│   └── analysis/             # Analysis scripts
│       ├── analyze_detection_control.py      # Detection vs control analysis
│       ├── compute_position_detection_accuracy.py  # Position detection analysis
│       ├── plot_strength_comparison_adjusted.py    # Strength comparison plots
│       └── analyze_final.py          # Final analysis scripts
├── data/
│   ├── dataset/              # Concept datasets
│   │   ├── simple_data.json  # Simple concepts (Dust, Satellites, etc.)
│   │   └── complex_data.json # Complex concepts (betrayal, recursion, etc.)
│   └── saved_vectors/        # Pre-computed steering vectors
│       └── llama/            # Vectors for Llama-3.1-8B-Instruct
├── results/
│   ├── csv/                  # Experiment results in CSV format
│   └── mechinterp/           # Mechanistic interpretability results (.pt)
├── figures/                  # All figures used in paper
├── latex/                    # LaTeX paragraph drafts
└── scripts/                  # Shell scripts for running experiments
```

## Model

All experiments use **Meta-Llama-3.1-8B-Instruct** (32 layers, hidden dim 4096).

## Key Experiments

### 1. Binary Detection (Section 4)
- **File**: `code/experiments/position_detection.py`
- **Results**: `results/csv/output_control_question.csv`
- **Figures**: `figures/detection_vs_control_*.png`

### 2. Sentence Localization (Section 5.2)
- **File**: `code/experiments/main.py` (localization mode)
- **Results**: `results/csv/output_localization_*.csv`
- **Figures**: `figures/success_rate_localization_*.png`

### 3. Strength Comparison (Section 5.1)
- **File**: `code/experiments/strength_comparison.py`
- **Results**: `results/strength_comparison_all_concepts_all_concepts_best.pt`
- **Figures**: `figures/strength_comparison_*.png`

### 4. Mechanistic Analysis (Section 6)
- **File**: `code/experiments/mechinterp.py`, `mechinterp_patching.py`
- **Results**: `results/mechinterp/`
- **Figures**: `figures/mechinterp_*.png`

## Steering Vectors

Pre-computed vectors are in `data/saved_vectors/llama/`:
- Format: `{concept}_{layer}_{vec_type}.pt`
- Vector types: `avg` (average across tokens), `last` (final token)
- 10 concepts × 32 layers × 2 types = 640 vectors

## Running Experiments

### Requirements
```bash
pip install torch transformers numpy pandas matplotlib tqdm
```

### Example: Strength Comparison
```bash
python code/experiments/strength_comparison.py \
    --concepts all \
    --layers 0 2 4 6 8 10 \
    --pairs best \
    --num_trials 30
```

### Example: Localization
```bash
python code/experiments/main.py \
    --type localization \
    --layers 0 1 2 3 4 5 8 11 14 17 20 \
    --coeffs 2 5 8 11 14 17 20 \
    --num_sentences 10 \
    --num_trials 50
```

## Concepts

**Simple (concrete nouns):** Dust, Satellites, Trumpets, Origami, Illusions

**Complex (abstract, contrastive):** fibonacci_numbers, recursion, betrayal, appreciation, shutdown

## Citation

If you use this code or build on our work, please cite our arXiv preprint:

```bibtex
@article{hahami2026detecting,
  title={Detecting the Disturbance: A Nuanced View of Introspective Abilities in LLMs},
  author={Hahami, Ely and Sinha, Ishaan and Jain, Lavik and Kaplan, Josh and Hahami, Jon},
  journal={arXiv preprint},
  year={2026}
}
```
