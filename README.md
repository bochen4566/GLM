## Autonomous Web Navigation with Large Language Models
### Overview
This repository reproduces and analyzes the baseline performance of an LLM-based web navigation agent as described in our paper. The project includes three main objectives:
- Reproduce results of the baseline model.
- Conduct error analysis to identify performance limitations.
- Propose improvements for enhanced web navigation capabilities.

### Key Components
- Baseline Model Reproduction: Utilizes GPT-4o, LLaMA2-7B, and ChatGLM3-6B on the MiniWoB++ dataset. (Corresponding code can be found in branches)
- Agent Framework: LLM agent processes parsed HTML and instructions to simulate user actions (e.g., clicks, text input).
- Error Analysis: Evaluates model accuracy across various web navigation tasks (clicking, input, selection, complex interaction).
- Proposed Improvements: Fine-tuning on HTML-based tasks, prompt optimization, and an enhanced action parsing framework.
  
### Setup
- Install dependencies from requirements.txt.
- Run main.py and modify relevant files to reproduce baseline results on MiniWoB++.
- Evaluate results and error metrics.

### Future Work
- Fine-tune models on web-specific data.
- Broaden evaluation across additional web navigation benchmarks.
- Refine prompt structures and enhance model interpretability in HTML contexts.
