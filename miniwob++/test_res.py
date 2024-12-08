import json
import os
from pathlib import Path

# Get current directory
result_path = '/content/GLM1129/miniwob++/outlog/out3/'

scores = {}
for filename in os.listdir(result_path):
    # Skip files ending with _0.json
    if filename.endswith('_0.json'):
        continue
        
    if filename.endswith('.json'):
        filepath = os.path.join(result_path, filename)
        with open(filepath, 'r') as f:
            data = json.load(f)
            if 'avg_score' in data:
                task_name = data.get('task', filename.replace('.json', ''))
                scores[task_name] = data['avg_score']

if scores:
    avg_score = sum(scores.values()) / len(scores)
    
    # Create summary dictionary
    summary = {
        "task_scores": scores,
        "average_score": round(avg_score, 3),
        "num_tasks": len(scores)
    }
    
    # Save to JSON file
    output_path = os.path.join(result_path, 'summary.json')
    with open(output_path, 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"Average score: {avg_score:.3f}")
    print(f"Number of tasks: {len(scores)}")
    print(f"Summary saved to: {output_path}")
else:
    print("No valid files found")