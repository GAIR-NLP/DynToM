# DynToM: Evaluating LLM Adaptation to Temporal Evolution of Human States

This repository contains the **DYNTOM** benchmark for evaluating Large Language Models' Theory of Mind (ToM) capabilities in dynamic social contexts. Unlike existing benchmarks that focus on static mental states, DYNTOM captures the temporal evolution of mental states across interconnected scenarios.

<div align="center">
  <img src="asset/main_figure.png" alt="Alt Text" width="600">
</div>

## 📖 Paper Introduction

**DYNTOM** addresses a critical gap in current ToM evaluations - the ability to track and understand how human mental states evolve over time in real-world social interactions. While existing benchmarks like SocialIQA, BigToM, and TOMBENCH focus on static snapshots, our work introduces a novel approach to evaluate LLMs' understanding of dynamic mental state changes across multiple interconnected scenarios.

### Key Contributions:
- A systematic framework for generating temporally connected social scenarios
- 78,100 questions across 1,100 social contexts with 5,500 scenarios
- Comprehensive evaluation revealing that LLMs underperform humans by 44.7%
- Analysis showing significant performance degradation when tracking mental state evolution

**Paper:** [Towards Dynamic Theory of Mind: Evaluating LLM Adaptation to Temporal Evolution of Human States](https://arxiv.org/abs/your-paper-link)

## 🗂️ Repository Structure

```
DynToM/
├── data/
│   ├── dyntom_full.json              # Complete DYNTOM dataset
│   ├── dyntom_sample.json            # Sample subset for quick testing
│   └── social_contexts/
│       ├── locations.json            # 261 social locations across 13 categories
│       ├── character_profiles.json   # Character profile templates
│       └── relationships.json        # Character relationship types
├── src/
│   ├── evaluation/
│   │   ├── evaluate_models.py        # Model evaluation scripts
│   │   ├── metrics.py               # Evaluation metrics calculation
│   │   └── prompts.py               # Vanilla and CoT prompting templates
│   ├── analysis/
│   │   ├── error_analysis.py        # Performance analysis tools
│   │   └── visualization.py         # Result visualization
│   └── utils/
│       ├── data_loader.py           # Data loading utilities
│       └── preprocessing.py         # Data preprocessing functions
├── results/
│   ├── model_performance.json       # Evaluation results for all models
│   └── human_baseline.json          # Human performance baseline
├── requirements.txt                 # Python dependencies
├── README.md                        # This file
└── LICENSE                         # License information
```

## 📊 Data Structure

### Main Dataset Format

The DYNTOM dataset is structured as follows:

```json
{
  "social_context_id": {
    "location": "restaurant",
    "location_type": "Food and Beverage",
    "characters": {
      "main_character": {
        "name": "Angela Hwang",
        "gender": "Woman",
        "occupation": "Hairdresser",
        "race": "Asian",
        "education": "High School",
        "personality": "ESFP"
      },
      "supporting_character": {
        "name": "Kevin Flores",
        "gender": "Man",
        "occupation": "Construction Worker",
        "race": "Latino",
        "education": "High School",
        "personality": "ISTP"
      }
    },
    "relationship": "Friends discussing career concerns",
    "scenarios": [
      {
        "scenario_id": 1,
        "background": "Description of the scenario context",
        "dialogue": [
          {"speaker": "Angela", "text": "Hey Kevin, thanks for meeting me..."},
          {"speaker": "Kevin", "text": "Honestly, Angela, I'm not happy..."}
        ],
        "mental_states": {
          "belief": "Kevin is unhappy with his job",
          "emotion": "concerned for Kevin",
          "intention": "to talk to Kevin about his job satisfaction",
          "action": "initiating conversation about work"
        }
      }
    ],
    "questions": [
      {
        "question_id": "understanding_belief_1",
        "type": "Understanding",
        "mental_state": "belief",
        "scenario": 1,
        "question": "What is Angela's belief in scenario 1?",
        "options": ["A) ...", "B) ...", "C) ...", "D) ..."],
        "answer": "C",
        "explanation": "Detailed explanation of the correct answer"
      },
      {
        "question_id": "transformation_emotion_1_2",
        "type": "Transformation-1",
        "mental_state": "emotion",
        "scenarios": [1, 2],
        "question": "How does Angela's emotion change from scenario 1 to scenario 2?",
        "options": ["A) No change", "B) From concern to relief", "C) From concern to growing concern"],
        "answer": "C",
        "explanation": "Angela's concern deepens as Kevin's situation worsens"
      }
    ]
  }
}
```

### Question Types

1. **Understanding Questions (28.2%)**: Identify mental states in specific scenarios
2. **Transformation-1 Questions (22.5%)**: Detect state changes between consecutive scenarios  
3. **Transformation-2 Questions (43.7%)**: Understand causal mechanisms behind state changes
4. **Transformation-3 Questions (5.6%)**: Track state evolution across all scenarios

### Mental States Evaluated

- **Beliefs**: Characters' understanding of situations and other people
- **Emotions**: Emotional responses to situations and interactions
- **Intentions**: Goals and plans characters intend to pursue
- **Actions**: Observable behaviors resulting from mental states

## 🏆 Main Experimental Results

### Overall Performance

| Model | Vanilla | CoT | Human Baseline |
|-------|---------|-----|----------------|
| GPT-4o | **64.0%** | 61.1% | **77.7%** |
| GPT-4-Turbo | 47.6% | 47.1% | - |
| Llama-3.1-70B | 57.1% | 57.6% | - |
| Qwen2-72B | 48.5% | 51.3% | - |
| Average (All LLMs) | 33.0% | 32.8% | - |

### Key Findings

1. **Significant Human-AI Gap**: Even the best model (GPT-4o) underperforms humans by 13.7%
2. **Transformation vs Understanding**: Models perform significantly worse on transformation questions (25.8% avg) compared to understanding questions (45.9% avg)
3. **CoT Limitations**: Chain-of-thought prompting shows inconsistent benefits and can harm performance in advanced models
4. **Lost in the Middle**: Performance degrades significantly for middle scenarios in longer sequences
5. **Mental State Differences**: Emotion reasoning achieves highest accuracy (54.7%), while belief reasoning lags behind (41.7%)

### Performance by Question Type

| Question Type | Human | GPT-4o | LLM Average |
|---------------|-------|--------|-------------|
| Understanding | 79.5% | 88.8% | 45.9% |
| Transformation-1 | 76.6% | 48.5% | 25.0% |
| Transformation-2 | 76.1% | 47.0% | 25.8% |
| Transformation-3 | 75.7% | 51.5% | 26.8% |



## 📝 Citation

```bibtex
@article{xiao2024dyntom,
  title={Towards Dynamic Theory of Mind: Evaluating LLM Adaptation to Temporal Evolution of Human States},
  author={Yang Xiao and Jiashuo Wang and Qiancheng Xu and Changhe Song and Chunpu Xu and Yi Cheng and Wenjie Li and Pengfei Liu},
  journal={arXiv preprint arXiv:xxxx.xxxxx},
  year={2024}
}
```

## 🤝 Contributing

We welcome contributions to improve DYNTOM! Please report issues, or add new features.


## 🙏 Acknowledgments

We thank all annotators who helped validate the quality and realism of our dataset. This work was supported by The Hong Kong Polytechnic University and Shanghai Jiao Tong University.

---

**Dataset Available**: [🤗 HuggingFace](https://huggingface.co/datasets/GAIR-NLP/DynToM) | **Paper**: [📄 ArXiv](https://arxiv.org/abs/xxxx.xxxxx)