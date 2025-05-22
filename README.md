# DynToM: Evaluating LLM Adaptation to Temporal Evolution of Human States
<div align="center">

[![GitHub](https://img.shields.io/badge/GitHub-Repository-blue?logo=github)](https://github.com/GAIR-NLP/DynToM)
[![Paper](https://img.shields.io/badge/Paper-ArXiv-red?logo=arxiv)](https://arxiv.org/abs/xxxx.xxxxx)
[![Dataset](https://img.shields.io/badge/Dataset-HuggingFace-yellow?logo=huggingface)](https://huggingface.co/datasets/YangXiao-nlp/DynToM)

</div>

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

## 📊 Data Structure

The DYNTOM dataset consists of three main components organized in the `data/script/data/` directory:

### Core Data Files

#### 1. `story.json` - Complete Social Stages
Contains the complete social interaction structure with character profiles, relationships, and temporally connected scenarios:

#### 2. `question_new.json` - Questions with Multiple Choice Options
Contains evaluation questions with complete answer options:



## 🏆 Main Experimental Results

### Overall Performance

| Subject | Belief |  | Emotion |  | Intention |  | Action |  | AVG. |
|---------|--------|--------|---------|--------|-----------|--------|--------|--------|------|
|         | U | T | U | T | U | T | U | T |      |
| Human | 83.8±16.4 | 77.6±12.0 | 89.5±10.7 | 78.7±14.0 | 79.0±21.4 | 73.8±14.0 | 76.7±25.8 | 76.3±14.0 | 77.7±12.7 |
| GPT-4o | 80.9 | 44.5 | 91.7 | 45.8 | 87.5 | 51.9 | 95.1 | 55.6 | 64.0 |
| GPT-4-Turbo | 63.5 | 32.3 | 74.7 | 33.9 | 71.3 | 35.5 | 80.5 | 36.2 | 47.6 |
| Llama-3.1-70B | 65.8 | 40.2 | 93.8 | 42.3 | 82.8 | 42.0 | 91.8 | 45.5 | 57.1 |
| Llama-3.1-8B | 31.6 | 18.0 | 40.0 | 19.9 | 22.4 | 16.6 | 26.6 | 15.5 | 22.3 |
| Mixtral-8x7B | 23.3 | 21.6 | 46.2 | 18.4 | 32.9 | 10.8 | 40.3 | 9.5 | 21.9 |
| Mistral-7B | 21.3 | 11.7 | 23.8 | 10.2 | 16.3 | 10.1 | 20.6 | 9.2 | 13.9 |
| Qwen2-72B | 72.0 | 37.2 | 85.5 | 38.0 | 79.5 | 33.2 | 89.8 | 20.9 | 48.5 |
| Qwen2-7B | 22.2 | 19.8 | 43.0 | 20.5 | 25.1 | 15.7 | 24.6 | 15.0 | 22.1 |
| DeepSeek-V2 | 6.5 | 9.2 | 4.8 | 8.1 | 3.7 | 7.3 | 2.8 | 5.7 | 7.2 |
| GLM-4 | 29.5 | 23.9 | 43.9 | 20.8 | 28.5 | 16.5 | 40.4 | 16.8 | 25.4 |
| **LLM AVG.** | **41.7** | **25.8** | **54.7** | **25.8** | **45.0** | **24.0** | **51.3** | **23.0** | **33.0** |
| GPT-4o+CoT | 79.2 | 44.5 | 88.0 | 47.6 | 82.1 | 46.6 | 90.4 | 49.6 | 61.1 |
| GPT-4-Turbo+CoT | 61.7 | 31.0 | 77.8 | 33.2 | 71.4 | 32.8 | 81.0 | 37.6 | 47.1 |
| Llama-3.1-70B+CoT | 68.0 | 38.9 | 90.7 | 43.7 | 81.4 | 42.8 | 96.5 | 46.6 | 57.6 |
| Llama-3.1-8B+CoT | 32.0 | 21.7 | 40.3 | 20.9 | 21.8 | 19.3 | 23.3 | 15.9 | 23.6 |
| Mixtral-8x7B+CoT | 15.6 | 13.9 | 29.7 | 13.8 | 25.8 | 8.8 | 26.6 | 8.8 | 15.8 |
| Mistral-7B+CoT | 21.6 | 10.1 | 22.5 | 11.0 | 19.9 | 8.1 | 18.8 | 8.8 | 13.3 |
| Qwen2-72B+CoT | 70.1 | 39.2 | 87.6 | 41.4 | 83.8 | 34.6 | 89.0 | 27.1 | 51.3 |
| Qwen2-7B+CoT | 28.6 | 18.1 | 43.7 | 19.3 | 29.6 | 19.7 | 20.2 | 18.4 | 23.5 |
| DeepSeek-V2+CoT | 7.4 | 9.8 | 3.2 | 10.4 | 5.0 | 7.3 | 5.0 | 6.4 | 8.1 |
| GLM-4+CoT | 30.0 | 26.4 | 48.0 | 22.1 | 32.4 | 17.7 | 43.2 | 14.1 | 26.6 |
| **LLM+CoT AVG.** | **41.4** | **25.4** | **53.2** | **26.3** | **45.3** | **23.8** | **49.4** | **23.3** | **32.8** |

### Key Findings

1. **Significant Human-AI Gap**: Even the best model (GPT-4o) underperforms humans by 13.7%
2. **Transformation vs Understanding**: Models perform significantly worse on transformation questions compared to understanding questions
3. **CoT Limitations**: Chain-of-thought prompting shows inconsistent benefits and can harm performance in advanced models
4. **Mental State Differences**: Emotion reasoning achieves highest accuracy, while belief reasoning lags behind





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

**Dataset Available**: [🤗 HuggingFace](https://huggingface.co/datasets/YangXiao-nlp/DynToM) | **Paper**: [📄 ArXiv](https://arxiv.org/abs/xxxx.xxxxx) ｜ 