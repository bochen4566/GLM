# LLM-Powered Web Navigation Framework

## Overview
This project implements and evaluates Large Language Model (LLM) based web navigation agents on the MiniWoB++ benchmark. We support multiple LLM backends including GPT-4, LLaMA2-7B, and ChatGLM3-6B, with a focus on autonomous web interaction capabilities.

## Key Features
- **Multi-Model Support**: Compatible with GPT-4, LLaMA2-7B, and ChatGLM3-6B
- **Action Framework**: Robust system for HTML parsing and web interaction simulation
- **Configurable Parameters**: Adjustable temperature, timeout, and other model parameters
- **Comprehensive Evaluation**: Detailed logging and performance metrics

## Installation & Setup For miniwob++

### Requirements
```bash
pip install -r requirements.txt
```

### Environment Setup
```bash
export OPENAI_API_KEY=your_api_key  # If using GPT-4
```

## Usage

### Running Tests
```bash
python main.py [cudas] [test-amount] [model-path] [result-path]
```

### Parameter Description
| Parameter   | Format       | Mandatory | Use                                                        |
| ----------- | ------------ | --------- | ---------------------------------------------------------- |
| cudas       | 0,1,2        | Yes       | The GPU number to be used, separated by commas, no spaces  |
| test-amount | 10           | Yes       | Number of test cases per task |
| model-path  | model_path/  | Yes       | Path to the model to be tested, if set to 'manual' then manual execution can be performed |
| result-path | result/      | Yes       | Location for the model's output |

### Example Output
```sh
2023-11-30 06:28:13,283 - INFO - {"task": "click-button", "case_id": 10, "result": 1.0}
```

## Project Structure
```
miniwob++/
├── main.py           # Main testing framework
├── llms/            # Model implementations
├── miniwob_tools/   # HTML parsing and utilities
└── configs/         # Configuration files
```

## Supported Actions
- **Click**: `ActionTypes.CLICK_COORDS`
- **Hover**: `ActionTypes.MOVE_COORDS`
- **Type**: `ActionTypes.FOCUS_ELEMENT_AND_TYPE_TEXT`
- **Scroll**: Up/Down with fixed coordinates

## Configuration
### Model Parameters
```python
response = client.chat.completions.create(
    model="gpt-4o",
    messages=messages,
    temperature=0.1,  # Lower for more deterministic outputs
    timeout=30000     # 30 seconds timeout
)
```

## Results
Sample performance metrics:
```
click-button-sequence            1.00
click-checkboxes                 0.62
click-checkboxes-large           0.07
click-color                      0.24
...
enter-date                       1.00
grid-coordinate                  0.30
all                             0.442
```

## License
Apache-2.0 License

## Citation
If you use this code in your research, please cite:
```
[Citation information]
```
